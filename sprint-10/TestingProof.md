# Testing Proof — Sprint 10

## 1. O testiranju u Sprintu 10

Sprint 10 donosi on-demand batch uvoz fajlova sa Google Drive-a (`POST /transcripts/batch-drive` uz zakazano
batch procesiranje i preskakanje duplikata), CHAT link u admin/agent header-u, ubrzanje CI/CD pipeline-a,
filtriranje šuma u pregledu issues-a, sekciju "Top Rated Responses", te stabilizaciju eskalacijskog i chat
toka (napuštanje razgovora, reconnect, auto-end, Resolve → KB pipeline, selektovano puštanje Q&A u bazu znanja).
Uz to je u fokusu bila robusnost PII maskiranja: uklanjanje lažno pozitivnih maski imena (npr. riječ "Simply"
pogrešno označena kao `[PERSON_1]`) i uklanjanje placeholder-tokena iz unosa baze znanja putem LLM prepisivanja,
kako bi odgovori u bazi znanja bili čisti i prirodni.

Automatsko testiranje u ovom sprintu fokusirano je na PII maskiranje — sloj koji je direktno mijenjan i nosi
najveći rizik za privatnost i kvalitet baze znanja. Funkcionalnosti koje su pretežno UI ili infrastrukturne
(CHAT link u header-u, ubrzanje deployment-a, vizuelni prikaz zakazanog batch-a, "Top Rated Responses" prikaz,
poboljšanja queue UI-a) validirane su ručno kroz aplikaciju, dok backend tokovi koje one koriste (transkripti,
chat sesije, eskalacije, baza znanja) ostaju pokriveni postojećim integracionim testovima.

Regresijskim trčanjem cijelog test suite-a (217 testova iz Sprinteva 1–9) verificira se da nove izmjene ne
narušavaju prethodno implementiranu autentikaciju, transkripte, korisnike, obavijesti, chat sesije, bazu znanja,
WebSocket i eskalacijsku infrastrukturu. U sklopu sprinta dodatno je očvrsnuta izolacija eskalacijskih
integracionih testova (svaki test koristi vlastiti svjež nalog umjesto dijeljenog admin naloga), te je
preprocessing test suite zadržan potpuno offline (bez mrežnih poziva ka Groq-u).

Testovi su pisani u Pythonu koristeći `pytest` i `pytest-asyncio`. Unitni testovi (PII pipeline, preprocessing,
ConnectionManager, eskalacijski servis) ne zahtijevaju bazu niti HTTP server — rade u potpunoj izolaciji.
Integracioni HTTP testovi koriste `httpx.AsyncClient` s `ASGITransport`. WebSocket testovi koriste
`starlette.testclient.TestClient`.

---

## 2. Funkcionalnosti obuhvaćene testiranjem

### Sprint 10 — novi testovi

#### PII maskiranje — uklanjanje placeholdera iz baze znanja (`test_preprocessing.py` — novi)

LLM scrubber prepisuje Q&A parove prije upisa u bazu znanja tako da PII placeholderi (`[PERSON_1]`, `[TELEFON_1]`,
…) budu zamijenjeni prirodnim formulacijama; deterministička regex zamjena je sigurnosna mreža da nijedan sirovi
token nikad ne dospije u bazu znanja kad LLM nije dostupan.

| Funkcionalnost | Tip testiranja | Šta je provjereno | Rezultat |
|---|---|---|---|
| `_strip_generic` — zamjena tokena | Unit | `[PERSON_1]`/`[TELEFON_1]` → generičke riječi ("korisnik", "broj telefona") | Prošlo |
| `_strip_generic` — bez tokena | Unit | Tekst bez placeholdera ostaje nepromijenjen | Prošlo |
| Scrub — preskakanje LLM-a bez placeholdera | Unit | Par bez placeholdera vraćen nepromijenjen, bez poziva Groq-a | Prošlo |
| Scrub — deterministički fallback bez ključa | Unit | Bez `GROQ_API_KEY` → regex zamjena, nijedan sirovi token ne ostaje | Prošlo |
| Scrub — LLM prepisivanje | Unit | Uz Groq → Q&A prirodno prepisana, placeholderi uklonjeni | Prošlo |
| Scrub — sigurnosna mreža za zaostali token | Unit | Ako model vrati `[TELEFON_1]`, token se deterministički ukloni prije upisa | Prošlo |

#### Ručno verificirane funkcionalnosti (bez novih automatskih testova)

| User Story | Tip provjere | Šta je provjereno | Rezultat |
|---|---|---|---|
| US-1 Batch Drive uvoz (`POST /transcripts/batch-drive`) | Ručno (E2E) | Unos folder ID-a → red obrade, preskakanje duplikata, prolaz kroz pipeline | Prošlo |
| US-2 CHAT link u header-u (Admin/Agent) | Ručno (UI) | Link vodi na `/chat`, vizuelno konzistentan | Prošlo |
| US-3 Ubrzanje CI/CD pipeline-a | Ručno (CI) | Layer/pip/npm caching, paralelizacija, smanjeno build vrijeme | Prošlo |
| US-4 Filtriranje issues-a | Ručno (UI) | Bez duplikata, poziva agenta, pozdrava i eksplicitnih zahtjeva | Prošlo |
| US-5 "Top Rated Responses" | Ručno (UI) | Sortirano po prosječnoj ocjeni, min. 3 feedbacka, ≥5 stavki | Prošlo |
| US-6 Eskalacijska queue UI | Ručno (UI) | Pozicija u redu, status bojom/ikonom, responzivnost, notifikacije | Prošlo |

### Sprint 1–9 — regresijsko testiranje (217 testova)

Svih 217 testova iz prethodnih sprinteva ostaju uključeni u test suite i ponovo prolaze bez funkcionalnih izmjena:

- `test_connection_manager.py` — 19 testova (WebSocket ConnectionManager)
- `test_escalation_service.py` — 29 testova (servisni sloj eskalacija)
- `test_preprocessing.py` — 36 testova (normalizacija, PII detekcija/maskiranje, chunking, audit, LLM speaker)
- `test_pipeline_integration.py` — 1 test (end-to-end `run_pipeline`)
- `test_auth.py` — 13 testova (autentikacija, profil, brisanje historije/naloga)
- `test_transcripts.py` — 15 testova (upload, pregled, ažuriranje, brisanje, pretraga)
- `test_users.py` — 12 testova (CRUD korisnika, RBAC)
- `test_escalation.py` — 27 testova (HTTP integracija eskalacija)
- `test_websocket.py` — 14 testova (WebSocket integracija)
- `test_announcements.py` — 12 testova (CRUD obavijesti)
- `test_chat_sessions.py` — 24 testa (sesije, ocjene, logovi, anomalije)
- `test_knowledge.py` — 15 testova (baza znanja: unos, odobravanje, pretraga)

> Napomena: `test_escalation.py` integracioni testovi su u Sprintu 10 dobili izolaciju po testu (vlastiti svjež
> nalog), a `test_pipeline_integration.py` se izvršava potpuno offline — bez izmjene funkcionalnog pokrića.

---

## 3. Pokretanje testova

**Komande:**

```bash
# Svi testovi odjednom (iz projekat/backend/)
pytest -v

# Samo novi sprint 10 testovi (PII placeholder scrub)
pytest tests/unit/test_preprocessing.py -v -k "strip_generic or scrub"

# Regresija PII pipelinea i end-to-end procesiranja
pytest tests/unit/test_preprocessing.py \
       tests/unit/test_pipeline_integration.py -v
```

**Lokacija:** `projekat/backend/`

**Rezultat (svi testovi):**

| | |
|---|---|
| Ukupno testova | 223 |
| Prošlo | 223 |
| Nije prošlo | 0 |
| Greške | 0 |

**Test fajlovi:**

| Fajl | Testova | Tip |
|---|---|---|
| `tests/unit/test_connection_manager.py` | 19 | Unit |
| `tests/unit/test_escalation_service.py` | 29 | Unit |
| `tests/unit/test_preprocessing.py` | 42 | Unit |
| `tests/unit/test_pipeline_integration.py` | 1 | Integracijsko (DB) |
| `tests/integration/test_auth.py` | 13 | Integracijsko |
| `tests/integration/test_transcripts.py` | 15 | Integracijsko |
| `tests/integration/test_users.py` | 12 | Integracijsko |
| `tests/integration/test_escalation.py` | 27 | Integracijsko |
| `tests/integration/test_websocket.py` | 14 | Integracijsko |
| `tests/integration/test_announcements.py` | 12 | Integracijsko |
| `tests/integration/test_chat_sessions.py` | 24 | Integracijsko |
| `tests/integration/test_knowledge.py` | 15 | Integracijsko |

---

## 4. Kompletan pytest output

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-8.2.0, pluggy-1.6.0
asyncio: mode=Mode.AUTO
collecting ... collected 223 items

tests/unit/test_connection_manager.py::test_connect_user_accepts_and_registers PASSED
tests/unit/test_connection_manager.py::test_connect_user_overwrites_previous PASSED
tests/unit/test_connection_manager.py::test_disconnect_user_removes_entry PASSED
tests/unit/test_connection_manager.py::test_disconnect_user_noop_when_missing PASSED
tests/unit/test_connection_manager.py::test_connect_agent_accepts_and_registers PASSED
tests/unit/test_connection_manager.py::test_connect_agent_closes_old_connection PASSED
tests/unit/test_connection_manager.py::test_connect_agent_tolerates_old_close_failure PASSED
tests/unit/test_connection_manager.py::test_disconnect_agent_removes_matching_ws PASSED
tests/unit/test_connection_manager.py::test_disconnect_agent_ignores_different_ws PASSED
tests/unit/test_connection_manager.py::test_send_to_user_success PASSED
tests/unit/test_connection_manager.py::test_send_to_user_not_connected_returns_false PASSED
tests/unit/test_connection_manager.py::test_send_to_user_removes_dead_connection PASSED
tests/unit/test_connection_manager.py::test_send_to_agent_success PASSED
tests/unit/test_connection_manager.py::test_send_to_agent_not_connected_returns_false PASSED
tests/unit/test_connection_manager.py::test_send_to_agent_removes_dead_connection PASSED
tests/unit/test_connection_manager.py::test_broadcast_to_agents_sends_to_all PASSED
tests/unit/test_connection_manager.py::test_broadcast_to_agents_excludes_sender PASSED
tests/unit/test_connection_manager.py::test_broadcast_to_agents_removes_dead_connections PASSED
tests/unit/test_connection_manager.py::test_broadcast_sends_same_payload_to_all PASSED
tests/unit/test_escalation_service.py::test_detect_trigger_below_threshold PASSED
tests/unit/test_escalation_service.py::test_detect_trigger_at_threshold_not_triggered PASSED
tests/unit/test_escalation_service.py::test_detect_trigger_above_threshold PASSED
tests/unit/test_escalation_service.py::test_create_escalation_new_entry PASSED
tests/unit/test_escalation_service.py::test_create_escalation_explicit_request_is_high_priority PASSED
tests/unit/test_escalation_service.py::test_create_escalation_stores_conversation PASSED
tests/unit/test_escalation_service.py::test_create_escalation_returns_existing_if_already_active PASSED
tests/unit/test_escalation_service.py::test_queue_position_first_in_line PASSED
tests/unit/test_escalation_service.py::test_queue_position_ordering PASSED
tests/unit/test_escalation_service.py::test_get_queue_returns_cekanje_and_utoku PASSED
tests/unit/test_escalation_service.py::test_get_queue_excludes_resolved PASSED
tests/unit/test_escalation_service.py::test_accept_escalation_transitions_to_utoku PASSED
tests/unit/test_escalation_service.py::test_accept_escalation_sets_agent_status_to_zauzet PASSED
tests/unit/test_escalation_service.py::test_accept_escalation_returns_none_if_already_utoku PASSED
tests/unit/test_escalation_service.py::test_accept_nonexistent_escalation_returns_none PASSED
tests/unit/test_escalation_service.py::test_resolve_escalation_sets_status_rijesena PASSED
tests/unit/test_escalation_service.py::test_resolve_escalation_resets_agent_status PASSED
tests/unit/test_escalation_service.py::test_resolve_nonexistent_escalation_returns_none PASSED
tests/unit/test_escalation_service.py::test_release_escalation_back_to_cekanje PASSED
tests/unit/test_escalation_service.py::test_release_escalation_resets_agent_status PASSED
tests/unit/test_escalation_service.py::test_release_escalation_wrong_agent_returns_none PASSED
tests/unit/test_escalation_service.py::test_release_escalation_not_utoku_returns_none PASSED
tests/unit/test_escalation_service.py::test_cancel_escalation_marks_napustena PASSED
tests/unit/test_escalation_service.py::test_cancel_escalation_no_active_returns_none PASSED
tests/unit/test_escalation_service.py::test_upsert_agent_status_creates_new_row PASSED
tests/unit/test_escalation_service.py::test_upsert_agent_status_updates_existing PASSED
tests/unit/test_escalation_service.py::test_upsert_agent_status_all_valid_statuses PASSED
tests/unit/test_escalation_service.py::test_get_active_for_user_returns_latest_active PASSED
tests/unit/test_escalation_service.py::test_get_active_for_user_returns_none_when_resolved PASSED
tests/unit/test_preprocessing.py::test_normalize_strips_and_unifies_newlines PASSED
tests/unit/test_preprocessing.py::test_normalize_collapses_blank_lines PASSED
tests/unit/test_preprocessing.py::test_normalize_collapses_spaces PASSED
tests/unit/test_preprocessing.py::test_normalize_nfc PASSED
tests/unit/test_preprocessing.py::test_normalize_empty PASSED
tests/unit/test_preprocessing.py::test_split_turns_roles PASSED
tests/unit/test_preprocessing.py::test_split_turns_unknown_fallback PASSED
tests/unit/test_preprocessing.py::test_split_turns_empty_lines_skipped PASSED
tests/unit/test_preprocessing.py::test_split_turns_positions_sequential PASSED
tests/unit/test_preprocessing.py::test_jmbg_checksum_valid PASSED
tests/unit/test_preprocessing.py::test_jmbg_checksum_invalid PASSED
tests/unit/test_preprocessing.py::test_find_structural_pii_jmbg PASSED
tests/unit/test_preprocessing.py::test_find_structural_pii_email PASSED
tests/unit/test_preprocessing.py::test_find_structural_pii_phone PASSED
tests/unit/test_preprocessing.py::test_find_structural_pii_iban PASSED
tests/unit/test_preprocessing.py::test_find_structural_pii_ssn PASSED
tests/unit/test_preprocessing.py::test_jmbg_13_digits_no_checksum_not_detected PASSED
tests/unit/test_preprocessing.py::test_mask_removes_jmbg PASSED
tests/unit/test_preprocessing.py::test_mask_removes_phone PASSED
tests/unit/test_preprocessing.py::test_mask_removes_email PASSED
tests/unit/test_preprocessing.py::test_mask_same_value_same_placeholder PASSED
tests/unit/test_preprocessing.py::test_mask_roundtrip PASSED
tests/unit/test_preprocessing.py::test_mask_token_map_invertible PASSED
tests/unit/test_preprocessing.py::test_no_pii_leak_in_masked_output PASSED
tests/unit/test_preprocessing.py::test_token_store_roundtrip PASSED
tests/unit/test_preprocessing.py::test_chunk_turns_single PASSED
tests/unit/test_preprocessing.py::test_chunk_turns_agent_is_odgovor PASSED
tests/unit/test_preprocessing.py::test_chunk_turns_unknown_is_kontekst PASSED
tests/unit/test_preprocessing.py::test_chunk_turns_long_turn_splits PASSED
tests/unit/test_preprocessing.py::test_chunk_turns_empty_text_skipped PASSED
tests/unit/test_preprocessing.py::test_safe_log_does_not_leak_text PASSED
tests/unit/test_preprocessing.py::test_text_hash_is_short_hex PASSED
tests/unit/test_preprocessing.py::test_mask_removes_ssn PASSED
tests/unit/test_preprocessing.py::test_llm_speaker_never_receives_raw_pii PASSED
tests/unit/test_preprocessing.py::test_llm_speaker_fallback_on_failure PASSED
tests/unit/test_preprocessing.py::test_speaker_strategy_uses_llm_for_audio_transcript PASSED
tests/unit/test_preprocessing.py::test_strip_generic_replaces_tokens PASSED
tests/unit/test_preprocessing.py::test_strip_generic_noop_without_tokens PASSED
tests/unit/test_preprocessing.py::test_scrub_skips_llm_when_no_placeholders PASSED
tests/unit/test_preprocessing.py::test_scrub_falls_back_deterministically_without_key PASSED
tests/unit/test_preprocessing.py::test_scrub_uses_llm_rewrite PASSED
tests/unit/test_preprocessing.py::test_scrub_safety_net_strips_token_llm_left_behind PASSED
tests/unit/test_pipeline_integration.py::test_run_pipeline_creates_segments_and_qa PASSED
tests/integration/test_auth.py::test_health PASSED
tests/integration/test_auth.py::test_login_invalid_credentials PASSED
tests/integration/test_auth.py::test_protected_route_requires_token PASSED
tests/integration/test_auth.py::test_login_valid_credentials PASSED
tests/integration/test_auth.py::test_login_missing_fields PASSED
tests/integration/test_auth.py::test_login_wrong_password PASSED
tests/integration/test_auth.py::test_register_duplicate_email PASSED
tests/integration/test_auth.py::test_update_me_requires_auth PASSED
tests/integration/test_auth.py::test_update_me PASSED
tests/integration/test_auth.py::test_delete_history_requires_auth PASSED
tests/integration/test_auth.py::test_delete_history PASSED
tests/integration/test_auth.py::test_delete_account_requires_auth PASSED
tests/integration/test_auth.py::test_delete_account PASSED
tests/integration/test_transcripts.py::test_upload_transcript_without_token PASSED
tests/integration/test_transcripts.py::test_upload_unsupported_file_type PASSED
tests/integration/test_transcripts.py::test_upload_txt_file PASSED
tests/integration/test_transcripts.py::test_list_transcripts_without_token PASSED
tests/integration/test_transcripts.py::test_list_transcripts_with_token PASSED
tests/integration/test_transcripts.py::test_get_transcript_not_found PASSED
tests/integration/test_transcripts.py::test_update_transcript_name PASSED
tests/integration/test_transcripts.py::test_update_transcript_processed_text PASSED
tests/integration/test_transcripts.py::test_update_transcript_not_found PASSED
tests/integration/test_transcripts.py::test_update_transcript_unauthenticated PASSED
tests/integration/test_transcripts.py::test_delete_transcript PASSED
tests/integration/test_transcripts.py::test_delete_transcript_removes_from_list PASSED
tests/integration/test_transcripts.py::test_delete_transcript_not_found PASSED
tests/integration/test_transcripts.py::test_delete_transcript_non_admin_forbidden PASSED
tests/integration/test_transcripts.py::test_search_transcripts_by_keyword PASSED
tests/integration/test_users.py::test_list_users_unauthenticated PASSED
tests/integration/test_users.py::test_list_users_as_non_admin_forbidden PASSED
tests/integration/test_users.py::test_list_users_as_admin_returns_list PASSED
tests/integration/test_users.py::test_update_role_as_admin PASSED
tests/integration/test_users.py::test_update_role_non_admin_forbidden PASSED
tests/integration/test_users.py::test_update_role_user_not_found PASSED
tests/integration/test_users.py::test_update_role_invalid_role_value PASSED
tests/integration/test_users.py::test_delete_user_as_admin PASSED
tests/integration/test_users.py::test_delete_user_removes_from_list PASSED
tests/integration/test_users.py::test_delete_self_forbidden PASSED
tests/integration/test_users.py::test_delete_user_not_found PASSED
tests/integration/test_users.py::test_delete_user_non_admin_forbidden PASSED
tests/integration/test_escalation.py::test_list_queue_requires_auth PASSED
tests/integration/test_escalation.py::test_list_queue_requires_admin_or_agent_role PASSED
tests/integration/test_escalation.py::test_list_queue_returns_list_for_admin PASSED
tests/integration/test_escalation.py::test_get_agent_statuses_requires_auth PASSED
tests/integration/test_escalation.py::test_get_agent_statuses_returns_list PASSED
tests/integration/test_escalation.py::test_update_agent_status_requires_auth PASSED
tests/integration/test_escalation.py::test_update_agent_status_valid PASSED
tests/integration/test_escalation.py::test_update_agent_status_invalid_value PASSED
tests/integration/test_escalation.py::test_request_escalation_requires_auth PASSED
tests/integration/test_escalation.py::test_request_escalation_creates_queue_entry PASSED
tests/integration/test_escalation.py::test_request_escalation_idempotent PASSED
tests/integration/test_escalation.py::test_cancel_escalation_requires_auth PASSED
tests/integration/test_escalation.py::test_cancel_escalation_when_no_active_returns_ok PASSED
tests/integration/test_escalation.py::test_cancel_escalation_cancels_active PASSED
tests/integration/test_escalation.py::test_get_escalation_not_found PASSED
tests/integration/test_escalation.py::test_get_escalation_returns_data PASSED
tests/integration/test_escalation.py::test_accept_escalation_transitions_to_utoku PASSED
tests/integration/test_escalation.py::test_accept_nonexistent_escalation PASSED
tests/integration/test_escalation.py::test_release_escalation PASSED
tests/integration/test_escalation.py::test_release_not_assigned_returns_400 PASSED
tests/integration/test_escalation.py::test_resolve_escalation PASSED
tests/integration/test_escalation.py::test_resolve_nonexistent_escalation PASSED
tests/integration/test_escalation.py::test_my_stats_requires_auth PASSED
tests/integration/test_escalation.py::test_my_stats_returns_counts PASSED
tests/integration/test_escalation.py::test_my_history_requires_auth PASSED
tests/integration/test_escalation.py::test_my_history_returns_list PASSED
tests/integration/test_escalation.py::test_my_history_limit_param PASSED
tests/integration/test_websocket.py::test_user_ws_connects_with_valid_token PASSED
tests/integration/test_websocket.py::test_user_ws_rejects_missing_token PASSED
tests/integration/test_websocket.py::test_user_ws_rejects_invalid_token PASSED
tests/integration/test_websocket.py::test_user_ws_rejects_expired_token PASSED
tests/integration/test_websocket.py::test_user_ws_different_sessions_are_independent PASSED
tests/integration/test_websocket.py::test_agent_ws_connects_with_valid_agent_token PASSED
tests/integration/test_websocket.py::test_agent_ws_receives_queue_sync_on_connect PASSED
tests/integration/test_websocket.py::test_agent_ws_rejects_invalid_token PASSED
tests/integration/test_websocket.py::test_agent_ws_rejects_regular_user_role PASSED
tests/integration/test_websocket.py::test_agent_ws_rejects_missing_token PASSED
tests/integration/test_websocket.py::test_agent_ws_admin_can_connect PASSED
tests/integration/test_websocket.py::test_agent_sends_message_to_connected_user PASSED
tests/integration/test_websocket.py::test_agent_receives_error_when_not_assigned PASSED
tests/integration/test_websocket.py::test_agent_typing_forwarded_to_user PASSED
tests/integration/test_announcements.py::test_list_active_requires_auth PASSED
tests/integration/test_announcements.py::test_list_active_as_authenticated_user PASSED
tests/integration/test_announcements.py::test_list_all_requires_admin PASSED
tests/integration/test_announcements.py::test_list_all_as_admin PASSED
tests/integration/test_announcements.py::test_create_announcement_requires_admin PASSED
tests/integration/test_announcements.py::test_create_announcement_as_admin PASSED
tests/integration/test_announcements.py::test_create_announcement_without_naslov PASSED
tests/integration/test_announcements.py::test_update_announcement PASSED
tests/integration/test_announcements.py::test_update_announcement_not_found PASSED
tests/integration/test_announcements.py::test_delete_announcement PASSED
tests/integration/test_announcements.py::test_delete_announcement_not_found PASSED
tests/integration/test_announcements.py::test_active_list_reflects_deactivation PASSED
tests/integration/test_chat_sessions.py::test_list_sessions_requires_auth PASSED
tests/integration/test_chat_sessions.py::test_list_sessions_returns_list PASSED
tests/integration/test_chat_sessions.py::test_get_session_messages_not_found PASSED
tests/integration/test_chat_sessions.py::test_get_session_messages_wrong_user_returns_404 PASSED
tests/integration/test_chat_sessions.py::test_get_session_messages_returns_structure PASSED
tests/integration/test_chat_sessions.py::test_close_session PASSED
tests/integration/test_chat_sessions.py::test_close_nonexistent_session_returns_404 PASSED
tests/integration/test_chat_sessions.py::test_close_session_is_idempotent PASSED
tests/integration/test_chat_sessions.py::test_delete_session PASSED
tests/integration/test_chat_sessions.py::test_delete_session_removes_from_list PASSED
tests/integration/test_chat_sessions.py::test_delete_nonexistent_session_returns_404 PASSED
tests/integration/test_chat_sessions.py::test_rate_session PASSED
tests/integration/test_chat_sessions.py::test_rate_session_rating_is_clamped_to_valid_range PASSED
tests/integration/test_chat_sessions.py::test_rate_nonexistent_session_returns_404 PASSED
tests/integration/test_chat_sessions.py::test_admin_get_session_messages_requires_admin PASSED
tests/integration/test_chat_sessions.py::test_admin_get_session_messages_not_found PASSED
tests/integration/test_chat_sessions.py::test_admin_get_session_messages_any_user PASSED
tests/integration/test_chat_sessions.py::test_chat_logs_requires_admin PASSED
tests/integration/test_chat_sessions.py::test_chat_logs_as_admin_returns_list PASSED
tests/integration/test_chat_sessions.py::test_ratings_requires_auth PASSED
tests/integration/test_chat_sessions.py::test_ratings_returns_stats PASSED
tests/integration/test_chat_sessions.py::test_issues_requires_admin PASSED
tests/integration/test_chat_sessions.py::test_issues_as_admin_returns_list PASSED
tests/integration/test_chat_sessions.py::test_issues_status_filter PASSED
tests/integration/test_knowledge.py::test_list_pending_requires_admin PASSED
tests/integration/test_knowledge.py::test_list_pending_as_admin PASSED
tests/integration/test_knowledge.py::test_list_categories_as_admin PASSED
tests/integration/test_knowledge.py::test_create_manual_qa_as_admin PASSED
tests/integration/test_knowledge.py::test_create_manual_qa_requires_admin PASSED
tests/integration/test_knowledge.py::test_create_manual_qa_too_short_rejected PASSED
tests/integration/test_knowledge.py::test_create_manual_qa_without_category PASSED
tests/integration/test_knowledge.py::test_list_approved_as_admin PASSED
tests/integration/test_knowledge.py::test_update_kb_item PASSED
tests/integration/test_knowledge.py::test_update_kb_item_not_found PASSED
tests/integration/test_knowledge.py::test_approve_pending_item PASSED
tests/integration/test_knowledge.py::test_reject_pending_item PASSED
tests/integration/test_knowledge.py::test_delete_kb_item PASSED
tests/integration/test_knowledge.py::test_search_knowledge_requires_auth PASSED
tests/integration/test_knowledge.py::test_search_knowledge_returns_list PASSED

======================== 223 passed, 0 warnings in 61.78s ======================
```

---

## 5. Zaključak

Svih 223 testa prolazi bez grešaka. U Sprintu 10 dodano je 6 novih unitnih testova koji pokrivaju ključnu izmjenu
sprinta — čišćenje PII placeholdera iz baze znanja:

**PII maskiranje i čišćenje baze znanja (6 testova):** Verificira se da LLM scrubber prirodno prepisuje Q&A
parove i uklanja sve `[PERSON_1]`/`[TELEFON_1]` tokene, da se LLM ne poziva kad placeholdera nema, da postoji
deterministički regex fallback bez `GROQ_API_KEY` te sigurnosna mreža koja uklanja eventualni token koji model
vrati natrag — čime se garantuje da nijedan sirovi placeholder ne dospijeva u bazu znanja. Ova izmjena radi u
sprezi s ispravkom lažno pozitivnog maskiranja imena (npr. "Simply") u pipeline sloju, dok `mask()` ostaje
deterministička i offline.

Ostale korisničke priče Sprinta 10 (batch Drive uvoz, CHAT link u header-u, ubrzanje CI/CD-a, filtriranje
issues-a, "Top Rated Responses", poboljšanja eskalacijske queue) pretežno su UI i infrastrukturne prirode te su
validirane ručno kroz aplikaciju i CI; backend tokovi koje koriste ostaju pokriveni postojećim integracionim
testovima.

Regresijskim pokretanjem svih 217 testova iz Sprinteva 1–9 potvrđeno je da autentikacija, transkripti, korisnici,
obavijesti, chat sesije, baza znanja, WebSocket infrastruktura i eskalacijska logika rade neizmijenjeno. Dodatno
je očvrsnuta izolacija eskalacijskih integracionih testova, a preprocessing test suite zadržan je potpuno offline.
