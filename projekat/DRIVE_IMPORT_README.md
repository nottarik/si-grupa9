# Google Drive batch import — README

Stanje funkcionalnosti za uvoz transkripata sa Google Drivea, da se može nastaviti kasnije.
Admin zalijepi Drive **folder ID** → backend izlista podržane fajlove → pusti ih kroz
**isti pipeline kao manualni upload** (`process_transcript`) → status se prati u UI-u.

> Povezani dokumenti: `GOOGLE_DRIVE_BATCH_PLAN.md` (originalni plan) i
> `DRIVE_IMPORT_AND_BUILD_NOTES.md` (bilješke + Docker build optimizacija).
> Ovaj README je nadređen — opisuje **trenutno stanje** nakon zadnjih izmjena.

---

## 1. Jednokratni setup (Google Cloud)

1. [console.cloud.google.com](https://console.cloud.google.com) → novi projekt.
2. **APIs & Services → Library** → uključi **Google Drive API**.
3. **APIs & Services → Credentials → Create Credentials → Service account**
   (NE „OAuth client ID" — to je bila greška, daje `{"web":...}` umjesto ključa).
4. Service account → **Keys → Add Key → Create new key → JSON** → preuzmi.
   Pravi ključ ima `{"type":"service_account", ... "private_key":"-----BEGIN PRIVATE KEY-----\n..."}`.
5. U Google Driveu podijeli ciljni folder sa **email adresom service accounta**
   (`...@<projekt>.iam.gserviceaccount.com`), pristup **Viewer**.
6. Folder ID = dio URL-a poslije `/folders/`.

### Ključ u `.env`
JSON mora biti **jedna linija**, sa očuvanim razmacima u `-----BEGIN PRIVATE KEY-----`
i `\n` prijelomima. Najsigurnije generisanje (iz `projekat/backend`):

```powershell
$key = Get-Content "$env:USERPROFILE\Downloads\<kljuc>.json" -Raw |
       ConvertFrom-Json | ConvertTo-Json -Compress -Depth 10
$envPath = (Resolve-Path .\.env).Path
$kept = Get-Content $envPath | Where-Object { $_ -notmatch '^GOOGLE_SERVICE_ACCOUNT_JSON=' }
[System.IO.File]::WriteAllLines($envPath, ($kept + "GOOGLE_SERVICE_ACCOUNT_JSON=$key"))
```

Zatim restart: `docker compose up -d backend`.

### Validacija ključa (debug)
```powershell
docker compose exec backend python -c "
from app.core.config import settings
import json
info = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_JSON)
pk = info['private_key']
print('type:', info.get('type'), '| email:', info.get('client_email'))
print('BEGIN ok:', pk.startswith('-----BEGIN PRIVATE KEY-----'), '| newlines:', pk.count(chr(10)))
"
```
Treba: `type: service_account`, validan email, `BEGIN ok: True`, `newlines > 0`.
**Greške koje smo već imali:** (a) pogrešan tip kredencijala → samo ključ `web`;
(b) razmaci izbačeni iz PEM headera → `-----BEGINPRIVATEKEY-----` → `load_pem_private_key` puca.

---

## 2. Kako se koristi

Admin → **Upload → ☁️ Drive**:
- unese **folder ID**,
- izabere **jezik** (BS / EN / DE / **Auto / Mixed**),
- klikne **Start Import**.

Endpoint odmah izlista folder i vrati imena fajlova. Ispod dugmeta se prikaže lista:
- novi fajl → badge **„Importing…"**, pa **„✓ Imported"** kad pipeline završi (`Obradjeno`),
  ili **„✗ Failed"** (`Odbacen`);
- već uvezen → **„Already imported"**.

Frontend pollira status svake ~2.5 s (do ~3 min) i sam ažurira redove.
Paralelno se transkripti pojavljuju u **Transcripts** sekciji (Sirovi → Obradjeno).

---

## 3. Kako radi (tok)

```
POST /api/v1/transcripts/import-drive  { folder_id, language }   (admin)
  ├─ 503 ako GOOGLE_SERVICE_ACCOUNT_JSON nije postavljen
  ├─ GoogleDriveService().list_files(folder_id)   → 502 ako folder ne valja / nije podijeljen
  ├─ dedup po postojećem `naziv` LIKE 'gdrive:<folder_id>:%'
  ├─ vrati { folder_id, message, files:[{name, status: queued|skipped}] }
  └─ BackgroundTask: import_drive_folder(folder_id, uploader_id, language)
        za svaki NOVI fajl:
          audio → Supabase Storage; txt → decode; pdf → extract_pdf_text
          Transkript(naziv="gdrive:<folder_id>:<ime>", jezik=language, status=Sirovi)
          await process_transcript(id, language)   # Whisper (jezik ili auto) → pipeline → Qdrant
```

- **Dedup / idempotentnost:** `naziv = gdrive:<folder_id>:<ime_fajla>`. Ponovni import
  istog foldera preskače već uvezene. Nema nove DB kolone ni migracije.
- **Prikaz imena:** u bazi ostaje pun `naziv` (zbog dedupa po folderu), ali API
  (`TranscriptRead`/`TranscriptDetail`) stripuje `gdrive:<folder_id>:` pa UI vidi `test.wav`.
- **Jezik:** `"auto"` → backend šalje prazan jezik Whisperu (per-file detekcija, za
  foldere s više jezika). Inače ISO kod (`bs`/`en`/`de`).

---

## 4. Fajlovi (gdje šta stoji)

**Backend**
- `app/services/storage/google_drive_service.py` — `GoogleDriveService` (auth, `list_files`, `download_file`).
- `app/tasks/transcript_tasks.py` — `import_drive_folder(folder_id, uploader_id, language)`,
  `process_transcript(transcript_id, language)`.
- `app/api/v1/routes/transcripts.py` — `POST /import-drive` (list+dedup+vrati listu),
  `DELETE /{id}` (kaskadno brisanje, vidi dolje).
- `app/services/transcript/transcription_service.py` — `transcribe(..., language=None)` → auto-detect.
- `app/services/transcript/file_utils.py` — `classify_file`, `extract_pdf_text`, `ALLOWED_*`.
- `app/schemas/transcript.py` — `DriveImportRequest.language`, `DriveFileStatus`,
  `DriveImportResponse.files`, `_display_naziv` + validatori na `TranscriptRead`/`TranscriptDetail`.
- `app/core/config.py` — `GOOGLE_SERVICE_ACCOUNT_JSON`.
- `requirements.txt` — `google-api-python-client`, `google-auth`.

**Frontend**
- `src/api/transcripts.ts` — `importDriveTranscripts(folderId, language)` → `DriveImportResult`.
- `src/components/admin/sections/UploadSection.tsx` — `DriveImport` (jezik dropdown,
  lista fajlova, status polling preko `listTranscripts({ q: folderId })`).

---

## 5. Brisanje transkripta (popravljeno)

`segment.id_transkripta` nema `ON DELETE CASCADE`, pa je brisanje **bilo kojeg obrađenog
transkripta** padalo na FK. `DELETE /transcripts/{id}` sada prvo počisti djecu redom:
`unos_baze_znanja` (+ Qdrant vektori preko `vector_store.delete_item`), `token_map`,
`segment`, pa `transkript`.

**Poznati edge case:** ako je neki `unos_baze_znanja` već korišten u chatu
(`odgovor.id_unosa_baze_znanja`), to brisanje bi i dalje palo na FK. Za svježe uvezene
transkripte se ne dešava. Ako zatreba — prije brisanja KB unosa postaviti
`odgovor.id_unosa_baze_znanja = NULL` (kolona je nullable).

---

## 6. Provjere / testovi

```powershell
docker compose exec frontend npm run lint     # prolazi (strict, max-warnings 0)
docker compose exec backend python -c "from app.main import app; print('ok')"
```

> ⚠️ `pytest` trenutno **ne prolazi** — pada u setup fixture na
> `ALTER TABLE status_agenta DROP CONSTRAINT fk_status_agenta_eskalacija` (constraint
> ne postoji). To je postojeći problem test-harnessa (eskalacija tabele), **nevezan**
> za Drive import. Treba zasebno popraviti fixture/migracije prije nego testovi rade.

---

## 7. Ostalo za kasnije (van trenutnog obima)

- **Scheduled / automatski sync:** reuse `/internal/*` + `INTERNAL_API_KEY` obrazac
  (`routes/internal.py`) + novi `schedule:` GitHub Actions workflow koji curl-a tunnel.
  Zahtijeva čuvanje liste foldera za periodični sync.
- **Drugi izvori (S3 i sl.):** izdvojiti `RemoteSource` protocol
  (`list_files`/`download_file`) i dodati npr. `S3Source`; pipeline se ne dira.
- **Popraviti pytest harness** (vidi §6).
- **Delete edge case** sa `odgovor` referencom (vidi §5).
- **Veliki folderi:** redovi se kreiraju kao `Sirovi`; postojeći `reconcile-transcripts`
  ponovo zakači zaglavljene — nije potreban custom batching.
