# Plan: Batch import transkripata sa Google Drivea

> Revidirana verzija. Cilj: **minimalne izmjene arhitekture**. Obim za sada:
> **samo Google Drive**, **samo on-demand** (admin klikne dugme). Scheduled
> pokretanje je svjesno odgođeno (vidi "Kasnije").

## Cilj

Admin unese Google Drive folder ID → sistem preuzme sve podržane fajlove →
pokrene **isti pipeline koji već radi za manuelne uploade** → status vidljiv u UI-u.

---

## Ključne činjenice o postojećem kodu (provjereno)

Plan se oslanja na ono što **stvarno postoji**, ne na pretpostavke:

- `process_transcript(transcript_id)` (`app/tasks/transcript_tasks.py`) je već cijeli
  pipeline (download → Whisper → preprocessing → Qdrant). **Ne mijenja se.**
- Ruta `/transcripts/upload` (`routes/transcripts.py`) već radi tačno ono što nam
  treba po fajlu: klasifikuje tip, audio šalje na Supabase Storage, txt/pdf vadi
  tekst, kreira `Transkript(status=Sirovi)`, pa `background_tasks.add_task(process_transcript, id)`.
  Helperi `_classify_file()` i `_extract_pdf_text()` su već tu — **reuse, ne rewrite.**
- `StorageService` (`services/storage/storage_service.py`) je tanak wrapper oko
  Supabase Storage — koristimo `upload()` isto kao `/upload`.
- `Transkript` model ima `naziv`, `file_path`, `raw_text`, `format`, `status`.
  **Nema potrebe za novom kolonom** (vidi Dedup ispod).
- Postoji `/internal/*` + `INTERNAL_API_KEY` obrazac (`routes/internal.py`,
  `_require_internal_key`). To je prava osnova za scheduled run **kada/ako zatreba**.
- `reconcile-transcripts` već ponovo zakači svaki `Sirovi` transkript stariji od
  5 min → ugrađena sigurnosna mreža za velike batcheve, ne treba custom batching.

### Ispravke u odnosu na prethodni plan
- **NE postoji** GitHub Actions cron mehanizam (samo `ci.yml` i `release.yml`).
  Prethodni plan je pretpostavljao da postoji. Scheduled run zato nije "reuse"
  nego nova infrastruktura → odgođeno.
- Storage je **Supabase**, ne S3.
- **Bez nove DB kolone i bez Alembic migracije** — dedup ide preko `naziv`.

---

## Preduslovi (Google Cloud, ručno jednom)

1. Projekt na [console.cloud.google.com](https://console.cloud.google.com)
2. Omogućiti **Google Drive API**
3. Kreirati **Service Account** (ne OAuth — nema korisničkog login flow-a)
4. Preuzeti JSON ključ service accounta
5. Admin podijeli Drive folder sa email adresom service accounta
   (npr. `bot@projekt.iam.gserviceaccount.com`), read-only je dovoljno

JSON ključ ide kao env varijabla `GOOGLE_SERVICE_ACCOUNT_JSON` (cijeli JSON kao string).
**Nikad ne ide u git** — samo u `.env` / `.env.tunnel`.

---

## Šta treba dodati (Drive-only, on-demand)

### Backend

#### 1. Dependency (`backend/requirements.txt`)
```
google-api-python-client==2.137.0
google-auth==2.32.0
```

#### 2. `app/core/config.py`
Jedno polje:
```python
GOOGLE_SERVICE_ACCOUNT_JSON: str = ""  # cijeli JSON key kao string
```

#### 3. `app/services/storage/google_drive_service.py` (novi fajl)
Klasa `GoogleDriveService`:
- `__init__` / `authenticate()` — učita service account iz `GOOGLE_SERVICE_ACCOUNT_JSON`,
  podigne jasan `RuntimeError` ako nije konfigurisan.
- `list_files(folder_id) -> list[dict]` — vrati `{id, name, mimeType}` za podržane
  tipove (paginacija preko `pageToken`). Query: `'<folder_id>' in parents and trashed=false`.
- `download_file(file_id) -> bytes` — `files().get_media` + `MediaIoBaseDownload`.

Podržani MIME tipovi (poklapaju se sa `/upload`): `audio/mpeg`, `audio/wav`,
`audio/mp4`, `audio/x-m4a`, `audio/ogg`, `text/plain`, `application/pdf`.

#### 4. `app/tasks/transcript_tasks.py` — nova funkcija `import_drive_folder`
```python
async def import_drive_folder(folder_id: str, uploader_id) -> None
```
Radi **u BackgroundTask-u** (endpoint odmah vraća, ne blokira na download-u):
1. `GoogleDriveService().list_files(folder_id)`
2. Učitaj postojeće `naziv` iz baze (jedan upit) → set za dedup.
3. Za svaki **novi** fajl, ponovi tačno logiku iz `/upload`:
   - audio → `StorageService().upload(...)`, `Transkript(format=audio, status=Sirovi)`
   - txt → `raw_text = bytes.decode(...)`; pdf → `_extract_pdf_text(...)`
   - `db.add(...)`, commit, pa `process_transcript(transkript.id)` (await ili background)
4. Loguj sažetak: koliko queued / skipped / errors.

> Da se izbjegne duplikacija koda, helpere `_classify_file` i `_extract_pdf_text`
> izdvojiti iz `routes/transcripts.py` u npr. `app/services/transcript/file_utils.py`
> i importovati ih i u ruti i u tasku. (Mali refactor, bez promjene ponašanja.)

#### 5. `app/api/v1/routes/transcripts.py` — jedan novi endpoint
```
POST /transcripts/import-drive
Body: { folder_id: str }
Auth: admin
→ background_tasks.add_task(import_drive_folder, folder_id, current_user.id)
→ Vraća odmah: { message: "Import started", folder_id }
```
Status se prati preko **postojeće** `GET /transcripts/` liste (filter po `naziv`
prefiksu / datumu) — bez zasebnog status endpointa za sada.

### Dedup (bez nove kolone)
Kod kreiranja, `naziv` dobije prefiks izvora:
```
naziv = f"gdrive:{folder_id}:{file_name}"
```
Prije inserta provjeri postoji li već taj `naziv`. Rezultat: idempotentno
ponovno pokretanje istog foldera, **bez schema migracije**.

### Database
**Nema promjena.** (Svjesna odluka — dedup preko `naziv`.)

### Frontend

`frontend/src/components/admin/...` (postojeći Admin shell):
- Input: "Google Drive Folder ID"
- Dugme: "Pokreni uvoz" → `POST /transcripts/import-drive`
- Nakon poziva, refetch postojeće liste transkripata (React Query invalidate)
  da se vide novi `Sirovi` redovi kako prelaze u `Obradjeno`.

---

## Redoslijed implementacije

| Korak | Šta | Gdje |
|-------|-----|------|
| 1 | Google Cloud setup + service account JSON | Manualno |
| 2 | `google-api-python-client`, `google-auth` u requirements | `requirements.txt` |
| 3 | `GOOGLE_SERVICE_ACCOUNT_JSON` u config + `.env`/`.env.tunnel` | `config.py`, env |
| 4 | Izdvoji `_classify_file`/`_extract_pdf_text` u `file_utils.py` | refactor |
| 5 | `GoogleDriveService` | `services/storage/google_drive_service.py` |
| 6 | `import_drive_folder` task (dedup po `naziv`) | `tasks/transcript_tasks.py` |
| 7 | `POST /transcripts/import-drive` endpoint | `routes/transcripts.py` |
| 8 | Admin UI: input + dugme + refetch liste | `components/admin/...` |
| 9 | Test: mali folder (1 audio + 1 txt + 1 pdf) | ručno |

---

## Kasnije (van trenutnog obima)

- **Scheduled run:** dodati `POST /internal/run-drive-import` (isti
  `_require_internal_key` obrazac) + novi `schedule:` GitHub Actions workflow koji
  curl-a tunnel URL sa `INTERNAL_API_KEY`. Zahtijeva i čuvanje liste foldera za sync.
- **Drugi izvori (S3 i sl.):** ako zatreba, izdvojiti `RemoteSource` protocol
  (`list_files`/`download`) i dodati `S3Source` — pipeline se ne dira.

## Napomene

- `process_transcript` se **ne mijenja**.
- Service account JSON nikad ne ide u git.
- Veliki folderi: redovi se kreiraju kao `Sirovi`; postojeći
  `reconcile-transcripts` ponovo zakači zaglavljene → nije potreban custom batching.
