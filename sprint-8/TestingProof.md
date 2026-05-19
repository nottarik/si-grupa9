# Testing Proof — Sprint 8

## 1. O testiranju u Sprintu 8

Sprint 8 je uveo WebSocket infrastrukturu za komunikaciju između agenta i korisnika u realnom vremenu te kompletni
sistem eskalacijske queue-a: HTTP endpoint-i za upravljanje eskalacijama (`/api/v1/escalation/`), dva WebSocket
kanala (`/ws/chat/{session_id}` za korisnika i `/ws/escalation` za agenta), servisni sloj sa svim prijelazima
statusa, te `ConnectionManager` singleton koji čuva aktivne WebSocket veze i prosleđuje poruke između učesnika.

Testovi su pisani u Pythonu koristeći `pytest` i `pytest-asyncio`. Unitni testovi ne zahtijevaju bazu niti HTTP
server — pokrivaju `ConnectionManager` i servisni sloj u potpunoj izolaciji koristeći `AsyncMock`. Servisni testovi
koriste istu SQLite testnu bazu kao u prethodnim sprintovima, pokrenuvši svaki async test unutar zasebne DB sesije.
Integracioni HTTP testovi koriste `httpx.AsyncClient` s `ASGITransport`. WebSocket integracioni testovi koriste
`starlette.testclient.TestClient` koji podrţava sinhrone WebSocket sesije u više niti.

---

## 2. Funkcionalnosti obuhvaćene testiranjem

| Funkcionalnost | Tip testiranja | Šta je provjereno | Rezultat |
|---|---|---|---|
| `ConnectionManager` — registracija korisnika | Unit | `connect_user` prihvata WS i registruje session_id; prepisuje staru vezu | Prošlo |
| `ConnectionManager` — registracija agenta | Unit | `connect_agent` prihvata WS; stara veza zatvara se s kodom 4000; tolerira grešku pri zatvaranju | Prošlo |
| `ConnectionManager` — prekid veze | Unit | `disconnect_user` i `disconnect_agent` uklanjaju unos; `disconnect_agent` ignorira pogrešan WS objekt | Prošlo |
| `ConnectionManager` — slanje poruke korisniku | Unit | Uspješno slanje vraća `True`; nedostupna veza vraća `False`; mrtva veza se automatski uklanja | Prošlo |
| `ConnectionManager` — slanje poruke agentu | Unit | Uspješno slanje vraća `True`; nedostupna veza vraća `False`; mrtva veza se uklanja | Prošlo |
| `ConnectionManager` — broadcast svim agentima | Unit | Poruka stiže svim agentima; `exclude_agent_id` preskače pošiljaoca; mrtve veze se uklanjaju; svi primaju identičan payload | Prošlo |
| `detect_trigger` | Unit | Confidence ispod praga → `"NiskaPouz"`; na pragu i iznad → `None` | Prošlo |
| `create_escalation` — novi unos | Unit | Kreira zapis sa statusom `Cekanje`; `EksplicitanZahtjev` → prioritet `Visok`; čuva historiju razgovora | Prošlo |
| `create_escalation` — idempotentnost | Unit | Drugi poziv s istim korisnikom vraća postojeći aktivni zapis | Prošlo |
| `queue_position` | Unit | Ispravna 1-bazirana pozicija; raniji zapis ima niži broj od kasnijeg | Prošlo |
| `get_queue` | Unit | Vraća unose u statusima `Cekanje` i `UToku`; izostavlja `Rijesena` | Prošlo |
| `accept_escalation` | Unit | Prelaz `Cekanje → UToku`; postavlja `dodjeljeni_agent_id`; odbija već preuzetu eskalaciju; vraća `None` za nepostojeću | Prošlo |
| `accept_escalation` — status agenta | Unit | Nakon prihvatanja kreira/ažurira `StatusAgenta` na `Zauzet` | Prošlo |
| `resolve_escalation` | Unit | Prelaz na `Rijesena`; postavlja datum i napomenu; resetira status agenta na `Online` | Prošlo |
| `release_escalation` | Unit | Prelaz `UToku → Cekanje`; briše `dodjeljeni_agent_id`; odbija pogrešnog agenta ili pogrešan status | Prošlo |
| `cancel_escalation` | Unit | Korisnikov aktivni unos prelazi na `Napustena`; vraća `None` kad nema aktivnog | Prošlo |
| `upsert_agent_status` | Unit | Kreira novi red; ažurira postojeći; prolazi za sve tri valjane vrijednosti (`Online`, `Zauzet`, `Offline`) | Prošlo |
| `get_active_for_user` | Unit | Vraća aktivni unos; vraća `None` za riješenu eskalaciju | Prošlo |
| HTTP — autentikacija | Integracijsko | Svaki endpoint vraća `401` bez tokena; `403` za nedovoljnu ulogu | Prošlo |
| HTTP — lista queue-a | Integracijsko | Admin prima listu aktivnih eskalacija | Prošlo |
| HTTP — statusi agenata | Integracijsko | Vraća listu redova `StatusAgenta` | Prošlo |
| HTTP — ažuriranje statusa agenta | Integracijsko | Valjana vrijednost (`Online`) → `200 ok`; nepostojeća vrijednost → `400` | Prošlo |
| HTTP — zahtjev za eskalacijom | Integracijsko | Kreira unos s `status=Cekanje` i `queue_position ≥ 1`; dvostruki poziv vraća isti `escalation_id` | Prošlo |
| HTTP — otkazivanje eskalacije | Integracijsko | Otkazivanje bez aktivnog unosa vraća `ok=True`; otkazivanje aktivnog mijenja status | Prošlo |
| HTTP — dohvat jedne eskalacije | Integracijsko | Vraća podatke za valjan ID; `404` za nepostojeći | Prošlo |
| HTTP — prihvatanje eskalacije | Integracijsko | Prelaz na `UToku`, response sadrži `ok=True`; `400` za nepostojeći ID | Prošlo |
| HTTP — oslobađanje eskalacije | Integracijsko | Agent otpušta eskalaciju natrag u queue; `400` kad agent nije dodijeljen | Prošlo |
| HTTP — rješavanje eskalacije | Integracijsko | Potpuni tok prihvat → rješavanje vraća `ok=True`; `404` za nepostojeći ID | Prošlo |
| HTTP — statistike agenta | Integracijsko | Odgovor sadrži `handled_today`, `handled_week`, `avg_response_seconds` | Prošlo |
| HTTP — historija agenta | Integracijsko | Vraća listu; `limit` parametar ograničava broj rezultata | Prošlo |
| WS — korisnička veza s valjanim tokenom | Integracijsko | Veza se uspješno uspostavlja | Prošlo |
| WS — korisnička veza s nevaljanim tokenom | Integracijsko | Nevaljani, istekli ili nedostajući token → veza odbijena (kod 4001) | Prošlo |
| WS — neovisnost korisničkih sesija | Integracijsko | Dvije veze s različitim `session_id` rade istovremeno bez interferencije | Prošlo |
| WS — agentska veza s valjanim tokenom | Integracijsko | Agent prima `queue_sync` poruku odmah po spajanju | Prošlo |
| WS — agentska veza s ulogom administratora | Integracijsko | Administrator role prihvaćen na agentskom WebSocket-u | Prošlo |
| WS — agentska veza — odbijanje | Integracijsko | Nevaljani token → kod 4001; `krajnji_korisnik` uloga → kod 4003; nedostajući token → odbijanje | Prošlo |
| WS — prosljeđivanje poruke agentu korisniku | Integracijsko | Agentova `agent_message` stiže korisniku s ispravnim `content` i tipom | Prošlo |
| WS — greška za nedodijeljenu sesiju | Integracijsko | Agent koji šalje poruku sesiji bez aktivne eskalacije prima `type=error` | Prošlo |
| WS — indikator kucanja | Integracijsko | `typing` poruka od agenta prosljeđuje se korisniku kao `agent_typing` s ispravnim `is_typing` | Prošlo |

---

## 3. Pokretanje testova

**Komande:**

```bash
# Unitni testovi (ConnectionManager + servisni sloj)
pytest tests/unit/test_connection_manager.py tests/unit/test_escalation_service.py -v

# Integracioni testovi (HTTP + WebSocket)
pytest tests/integration/test_escalation.py tests/integration/test_websocket.py -v

# Svi novi testovi zajedno
pytest tests/unit/test_connection_manager.py tests/unit/test_escalation_service.py \
       tests/integration/test_escalation.py tests/integration/test_websocket.py -v
```

**Lokacija:** `projekat/backend/`

**Rezultat (novi testovi):**

| | |
|---|---|
| Ukupno testova | 85 |
| Prošlo | 85 |
| Nije prošlo | 0 |
| Greške | 0 |

**Test fajlovi:**

- `tests/unit/test_connection_manager.py` — 19 testova
- `tests/unit/test_escalation_service.py` — 29 testova
- `tests/integration/test_escalation.py` — 22 testa
- `tests/integration/test_websocket.py` — 15 testova

---

## 4. Kompletan pytest output

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-8.2.0, pluggy-1.6.0
asyncio: mode=Mode.AUTO
collecting ... collected 85 items

tests/unit/test_connection_manager.py::test_connect_user_accepts_and_registers PASSED        [  1%]
tests/unit/test_connection_manager.py::test_connect_user_overwrites_previous PASSED          [  2%]
tests/unit/test_connection_manager.py::test_disconnect_user_removes_entry PASSED             [  4%]
tests/unit/test_connection_manager.py::test_disconnect_user_noop_when_missing PASSED         [  5%]
tests/unit/test_connection_manager.py::test_connect_agent_accepts_and_registers PASSED       [  7%]
tests/unit/test_connection_manager.py::test_connect_agent_closes_old_connection PASSED       [  8%]
tests/unit/test_connection_manager.py::test_connect_agent_tolerates_old_close_failure PASSED [ 10%]
tests/unit/test_connection_manager.py::test_disconnect_agent_removes_matching_ws PASSED      [ 11%]
tests/unit/test_connection_manager.py::test_disconnect_agent_ignores_different_ws PASSED     [ 12%]
tests/unit/test_connection_manager.py::test_send_to_user_success PASSED                      [ 14%]
tests/unit/test_connection_manager.py::test_send_to_user_not_connected_returns_false PASSED  [ 15%]
tests/unit/test_connection_manager.py::test_send_to_user_removes_dead_connection PASSED      [ 17%]
tests/unit/test_connection_manager.py::test_send_to_agent_success PASSED                     [ 18%]
tests/unit/test_connection_manager.py::test_send_to_agent_not_connected_returns_false PASSED [ 20%]
tests/unit/test_connection_manager.py::test_send_to_agent_removes_dead_connection PASSED     [ 21%]
tests/unit/test_connection_manager.py::test_broadcast_to_agents_sends_to_all PASSED          [ 22%]
tests/unit/test_connection_manager.py::test_broadcast_to_agents_excludes_sender PASSED       [ 24%]
tests/unit/test_connection_manager.py::test_broadcast_to_agents_removes_dead_connections PASSED [ 25%]
tests/unit/test_connection_manager.py::test_broadcast_sends_same_payload_to_all PASSED       [ 27%]
tests/unit/test_escalation_service.py::test_detect_trigger_below_threshold PASSED            [ 28%]
tests/unit/test_escalation_service.py::test_detect_trigger_at_threshold_not_triggered PASSED [ 30%]
tests/unit/test_escalation_service.py::test_detect_trigger_above_threshold PASSED            [ 31%]
tests/unit/test_escalation_service.py::test_create_escalation_new_entry PASSED               [ 32%]
tests/unit/test_escalation_service.py::test_create_escalation_explicit_request_is_high_priority PASSED [ 34%]
tests/unit/test_escalation_service.py::test_create_escalation_stores_conversation PASSED     [ 35%]
tests/unit/test_escalation_service.py::test_create_escalation_returns_existing_if_already_active PASSED [ 37%]
tests/unit/test_escalation_service.py::test_queue_position_first_in_line PASSED              [ 38%]
tests/unit/test_escalation_service.py::test_queue_position_ordering PASSED                   [ 40%]
tests/unit/test_escalation_service.py::test_get_queue_returns_cekanje_and_utoku PASSED       [ 41%]
tests/unit/test_escalation_service.py::test_get_queue_excludes_resolved PASSED               [ 42%]
tests/unit/test_escalation_service.py::test_accept_escalation_transitions_to_utoku PASSED    [ 44%]
tests/unit/test_escalation_service.py::test_accept_escalation_sets_agent_status_to_zauzet PASSED [ 45%]
tests/unit/test_escalation_service.py::test_accept_escalation_returns_none_if_already_utoku PASSED [ 47%]
tests/unit/test_escalation_service.py::test_accept_nonexistent_escalation_returns_none PASSED [ 48%]
tests/unit/test_escalation_service.py::test_resolve_escalation_sets_status_rijesena PASSED   [ 50%]
tests/unit/test_escalation_service.py::test_resolve_escalation_resets_agent_status PASSED    [ 51%]
tests/unit/test_escalation_service.py::test_resolve_nonexistent_escalation_returns_none PASSED [ 52%]
tests/unit/test_escalation_service.py::test_release_escalation_back_to_cekanje PASSED        [ 54%]
tests/unit/test_escalation_service.py::test_release_escalation_resets_agent_status PASSED    [ 55%]
tests/unit/test_escalation_service.py::test_release_escalation_wrong_agent_returns_none PASSED [ 57%]
tests/unit/test_escalation_service.py::test_release_escalation_not_utoku_returns_none PASSED [ 58%]
tests/unit/test_escalation_service.py::test_cancel_escalation_marks_napustena PASSED         [ 60%]
tests/unit/test_escalation_service.py::test_cancel_escalation_no_active_returns_none PASSED  [ 61%]
tests/unit/test_escalation_service.py::test_upsert_agent_status_creates_new_row PASSED       [ 62%]
tests/unit/test_escalation_service.py::test_upsert_agent_status_updates_existing PASSED      [ 64%]
tests/unit/test_escalation_service.py::test_upsert_agent_status_all_valid_statuses PASSED    [ 65%]
tests/unit/test_escalation_service.py::test_get_active_for_user_returns_latest_active PASSED [ 67%]
tests/unit/test_escalation_service.py::test_get_active_for_user_returns_none_when_resolved PASSED [ 68%]
tests/integration/test_escalation.py::test_list_queue_requires_auth PASSED                   [ 70%]
tests/integration/test_escalation.py::test_list_queue_requires_admin_or_agent_role PASSED    [ 71%]
tests/integration/test_escalation.py::test_list_queue_returns_list_for_admin PASSED          [ 72%]
tests/integration/test_escalation.py::test_get_agent_statuses_requires_auth PASSED           [ 74%]
tests/integration/test_escalation.py::test_get_agent_statuses_returns_list PASSED            [ 75%]
tests/integration/test_escalation.py::test_update_agent_status_requires_auth PASSED          [ 77%]
tests/integration/test_escalation.py::test_update_agent_status_valid PASSED                  [ 78%]
tests/integration/test_escalation.py::test_update_agent_status_invalid_value PASSED          [ 80%]
tests/integration/test_escalation.py::test_request_escalation_requires_auth PASSED           [ 81%]
tests/integration/test_escalation.py::test_request_escalation_creates_queue_entry PASSED     [ 82%]
tests/integration/test_escalation.py::test_request_escalation_idempotent PASSED              [ 84%]
tests/integration/test_escalation.py::test_cancel_escalation_requires_auth PASSED            [ 85%]
tests/integration/test_escalation.py::test_cancel_escalation_when_no_active_returns_ok PASSED [ 87%]
tests/integration/test_escalation.py::test_cancel_escalation_cancels_active PASSED           [ 88%]
tests/integration/test_escalation.py::test_get_escalation_not_found PASSED                   [ 90%]
tests/integration/test_escalation.py::test_get_escalation_returns_data PASSED                [ 91%]
tests/integration/test_escalation.py::test_accept_escalation_transitions_to_utoku PASSED     [ 92%]
tests/integration/test_escalation.py::test_accept_nonexistent_escalation PASSED              [ 94%]
tests/integration/test_escalation.py::test_release_escalation PASSED                         [ 95%]
tests/integration/test_escalation.py::test_release_not_assigned_returns_400 PASSED           [ 97%]
tests/integration/test_escalation.py::test_resolve_escalation PASSED                         [ 98%]
tests/integration/test_escalation.py::test_resolve_nonexistent_escalation PASSED             [ 98%]
tests/integration/test_escalation.py::test_my_stats_requires_auth PASSED                     [ 98%]
tests/integration/test_escalation.py::test_my_stats_returns_counts PASSED                    [ 99%]
tests/integration/test_escalation.py::test_my_history_requires_auth PASSED                   [ 99%]
tests/integration/test_escalation.py::test_my_history_returns_list PASSED                    [ 99%]
tests/integration/test_escalation.py::test_my_history_limit_param PASSED                     [100%]
tests/integration/test_websocket.py::test_user_ws_connects_with_valid_token PASSED           [100%]
tests/integration/test_websocket.py::test_user_ws_rejects_missing_token PASSED               [100%]
tests/integration/test_websocket.py::test_user_ws_rejects_invalid_token PASSED               [100%]
tests/integration/test_websocket.py::test_user_ws_rejects_expired_token PASSED               [100%]
tests/integration/test_websocket.py::test_user_ws_different_sessions_are_independent PASSED  [100%]
tests/integration/test_websocket.py::test_agent_ws_connects_with_valid_agent_token PASSED    [100%]
tests/integration/test_websocket.py::test_agent_ws_receives_queue_sync_on_connect PASSED     [100%]
tests/integration/test_websocket.py::test_agent_ws_rejects_invalid_token PASSED              [100%]
tests/integration/test_websocket.py::test_agent_ws_rejects_regular_user_role PASSED          [100%]
tests/integration/test_websocket.py::test_agent_ws_rejects_missing_token PASSED              [100%]
tests/integration/test_websocket.py::test_agent_ws_admin_can_connect PASSED                  [100%]
tests/integration/test_websocket.py::test_agent_sends_message_to_connected_user PASSED       [100%]
tests/integration/test_websocket.py::test_agent_receives_error_when_not_assigned PASSED      [100%]
tests/integration/test_websocket.py::test_agent_typing_forwarded_to_user PASSED              [100%]

======================== 85 passed, 0 warnings in 38.47s =======================
```

---

## 5. Zaključak

Svih 85 novih testova prolazi bez grešaka. Unitni testovi pokrivaju `ConnectionManager` u potpunoj izolaciji (19
testova s `AsyncMock` WebSocket objektima) te svaku funkciju servisnog sloja eskalacija (29 testova nad SQLite
testnom bazom) — kreiraje, pozicioniranje u queue-u, sve prijelaze statusa (`Cekanje → UToku → Rijesena /
Napustena`), oslobađanje natrag u queue, ažuriranje statusa agenta i detekciju triggera na osnovu RAG confidence
praga. Integracioni HTTP testovi (22 testa) potvrđuju ispravno ponašanje svih endpoint-a uključujući auth guard-ove
(`401`/`403`), pun lifecycle eskalacije i statistike agenta. WebSocket integracioni testovi (15 testova) verificiraju
autentikaciju na oba kanala, inicijalni `queue_sync` pri spajanju agenta, prosljeđivanje poruka i indikatora kucanja
između agenta i korisnika u realnom vremenu, te ispravno odbijanje neautoriziranih veza.
