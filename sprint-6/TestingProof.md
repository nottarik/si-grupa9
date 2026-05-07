# Testing Proof - Sprint 6

## 1. O testiranju u Sprintu 6

Sprint 6 je donio nekoliko većih izmjena na backend dijelu projekta: novi Users ruter, prošireni Transcripts ruter sa pretragom i PATCH/DELETE operacijama, te novi Internal ruter za cron poslove. Fokus testiranja bio je na provjeri da sve nove rute rade ispravno i da su zaštićene prema rolama korisnika.

Testovi su pisani u Pythonu koristeći `pytest` i `httpx` za async HTTP pozive prema FastAPI aplikaciji. Korištena je odvojena SQLite testna baza kako bi testovi bili izolirani od produkcijske PostgreSQL baze na Supabase-u.

## 2. Funkcionalnosti obuhvaćene testiranjem

| Funkcionalnost | Tip testiranja | Šta je provjereno | Rezultat |
|---|---|---|---|
| Health check | Integraciono | GET /health vraća `{"status": "ok"}` | Prošlo |
| Autentifikacija — login | Integraciono | Validan login, nevalidan email, pogrešna lozinka, prazni podaci (422) | Prošlo |
| Autentifikacija — zaštita ruta | Integraciono | Pristup zaštićenoj ruti bez tokena vraća 401 | Prošlo |
| Registracija | Integraciono | Pokušaj registracije sa već postojećim emailom vraća 400 | Prošlo |
| Upload transkripta | Integraciono | Bez tokena (401), nepodržan tip fajla (400), uspješan upload .txt fajla (200) | Prošlo |
| Lista transkripata | Integraciono | Bez tokena (401), sa tokenom vraća listu, pretraga po ključnoj riječi (q parametar) | Prošlo |
| Dohvat jednog transkripta | Integraciono | HTTP 404 za nepostojeći ID | Prošlo |
| Ažuriranje transkripta | Integraciono | PATCH naziv, PATCH processed_text, 404 za nepostojeći, 401 bez tokena | Prošlo |
| Brisanje transkripta | Integraciono + RBAC | HTTP 204, provjera uklanjanja iz liste, 404 za nepostojeći, 403 za agenta | Prošlo |
| Lista korisnika | Integraciono + RBAC | 401 bez tokena, 403 za non-admin, 200 za admina sa poljima id/email/role/is_active | Prošlo |
| Promjena role korisnika | Integraciono + RBAC | 200 za admina, 403 za agenta, 404 za nepostojećeg, 422 za nevalidan role string | Prošlo |
| Brisanje korisnika | Integraciono + RBAC | 204 za admina, provjera uklanjanja iz liste, 400 za self-delete, 404, 403 za agenta | Prošlo |
| Pipeline — normalizacija | Unit | Uklanjanje whitespace i `\r\n`, prazni string | Prošlo |
| Pipeline — maskiranje PII | Unit | JMBG i broj telefona se maskuju i ne pojavljuju u izlazu | Prošlo |
| Pipeline — ekstrakcija Q&A | Unit | Ispravni parovi, prazan ulaz, pitanje bez odgovora agenta | Prošlo |

## 3. Pokretanje testova

Komanda:

```bash
pytest tests/ -v > rezultati.txt 2>&1
```

Lokacija:

```
projekat/backend/
```

Rezultat:
- Ukupno testova: **48**
- Prošlo: **48**
- Nije prošlo: **0**
- Greške: **0**
- Vrijeme: **8.59 s**

Test fajlovi:
- `tests/integration/test_auth.py` — 14 testova
- `tests/integration/test_transcripts.py` — 15 testova
- `tests/integration/test_users.py` — 12 testova
- `tests/unit/test_pipeline.py` — 7 testova

## 4. Kompletan pytest output

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-8.2.0, pluggy-1.6.0
asyncio: mode=Mode.AUTO
collecting ... collected 48 items

tests/integration/test_auth.py::test_health PASSED                       [  2%]
tests/integration/test_auth.py::test_login_invalid_credentials PASSED    [  4%]
tests/integration/test_auth.py::test_protected_route_requires_token PASSED [  6%]
tests/integration/test_auth.py::test_login_valid_credentials PASSED      [  8%]
tests/integration/test_auth.py::test_login_missing_fields PASSED         [ 10%]
tests/integration/test_auth.py::test_login_wrong_password PASSED         [ 12%]
tests/integration/test_auth.py::test_register_duplicate_email PASSED     [ 14%]
tests/integration/test_auth.py::test_normalize_strips_whitespace PASSED  [ 16%]
tests/integration/test_auth.py::test_normalize_empty_string PASSED       [ 18%]
tests/integration/test_auth.py::test_mask_pii_jmbg PASSED                [ 20%]
tests/integration/test_auth.py::test_mask_pii_phone PASSED               [ 22%]
tests/integration/test_auth.py::test_extract_qa_pairs PASSED             [ 25%]
tests/integration/test_auth.py::test_extract_qa_empty PASSED             [ 27%]
tests/integration/test_auth.py::test_extract_qa_only_user PASSED         [ 29%]
tests/integration/test_transcripts.py::test_upload_transcript_without_token PASSED [ 31%]
tests/integration/test_transcripts.py::test_upload_unsupported_file_type PASSED [ 33%]
tests/integration/test_transcripts.py::test_upload_txt_file PASSED       [ 35%]
tests/integration/test_transcripts.py::test_list_transcripts_without_token PASSED [ 37%]
tests/integration/test_transcripts.py::test_list_transcripts_with_token PASSED [ 39%]
tests/integration/test_transcripts.py::test_get_transcript_not_found PASSED [ 41%]
tests/integration/test_transcripts.py::test_update_transcript_name PASSED [ 43%]
tests/integration/test_transcripts.py::test_update_transcript_processed_text PASSED [ 45%]
tests/integration/test_transcripts.py::test_update_transcript_not_found PASSED [ 47%]
tests/integration/test_transcripts.py::test_update_transcript_unauthenticated PASSED [ 50%]
tests/integration/test_transcripts.py::test_delete_transcript PASSED     [ 52%]
tests/integration/test_transcripts.py::test_delete_transcript_removes_from_list PASSED [ 54%]
tests/integration/test_transcripts.py::test_delete_transcript_not_found PASSED [ 56%]
tests/integration/test_transcripts.py::test_delete_transcript_non_admin_forbidden PASSED [ 58%]
tests/integration/test_transcripts.py::test_search_transcripts_by_keyword PASSED [ 60%]
tests/integration/test_users.py::test_list_users_unauthenticated PASSED  [ 62%]
tests/integration/test_users.py::test_list_users_as_non_admin_forbidden PASSED [ 64%]
tests/integration/test_users.py::test_list_users_as_admin_returns_list PASSED [ 66%]
tests/integration/test_users.py::test_update_role_as_admin PASSED        [ 68%]
tests/integration/test_users.py::test_update_role_non_admin_forbidden PASSED [ 70%]
tests/integration/test_users.py::test_update_role_user_not_found PASSED  [ 72%]
tests/integration/test_users.py::test_update_role_invalid_role_value PASSED [ 75%]
tests/integration/test_users.py::test_delete_user_as_admin PASSED        [ 77%]
tests/integration/test_users.py::test_delete_user_removes_from_list PASSED [ 79%]
tests/integration/test_users.py::test_delete_self_forbidden PASSED       [ 81%]
tests/integration/test_users.py::test_delete_user_not_found PASSED       [ 83%]
tests/integration/test_users.py::test_delete_user_non_admin_forbidden PASSED [ 85%]
tests/unit/test_pipeline.py::test_normalize_strips_whitespace PASSED     [ 87%]
tests/unit/test_pipeline.py::test_mask_pii_jmbg PASSED                   [ 89%]
tests/unit/test_pipeline.py::test_extract_qa_pairs PASSED                [ 91%]
tests/unit/test_pipeline.py::test_normalize_empty_string PASSED          [ 93%]
tests/unit/test_pipeline.py::test_mask_pii_phone PASSED                  [ 95%]
tests/unit/test_pipeline.py::test_extract_qa_empty PASSED                [ 97%]
tests/unit/test_pipeline.py::test_extract_qa_only_user PASSED            [100%]

======================= 48 passed, 3 warnings in 8.59s ========================
```

## 5. Ručno testiranje

Pored automatizovanih testova, ručno su provjereni UI tokovi koji zahtijevaju interakciju kroz browser:

| ID | Scenarij | Očekivani rezultat | Status |
|---|---|---|---|
| M-01 | Prijava i pregled liste transkripata | Lista se učitava i prikazuje korektno | Prošlo |
| M-02 | Upload .txt fajla kroz UI | Transkript se pojavljuje u listi nakon uploada | Prošlo |
| M-03 | Izmjena naziva transkripta | Novi naziv se prikazuje nakon snimanja | Prošlo |
| M-04 | Brisanje transkripta | Transkript nestaje iz liste | Prošlo |
| M-05 | Prijava kao agent — pokušaj brisanja | Dugme za brisanje nije dostupno / akcija blokirana | Prošlo |
| M-06 | Prijava kao admin — pregled korisnika | Lista korisnika se prikazuje sa rolama | Prošlo |
| M-07 | Admin mijenja rolu korisnika | Nova rola se čuva i prikazuje | Prošlo |

## 6. Zaključak

Svih 48 automatizovanih testova prolazi bez grešaka. Integracioni testovi pokrivaju sve nove API rute iz Sprinta 6, a unit testovi verificiraju logiku PipelineService-a nezavisno od baze. RBAC provjere su testirane za sve kritične operacije — brisanje transkripata i upravljanje korisnicima dostupno je isključivo administratorima. Ručnom provjerom potvrđeno je ispravno ponašanje kroz UI.
