# Dev notes — git workflow i okruženje

Praktične bilješke za rad na ovom projektu. Dopunjavati po potrebi.

---

## 1. Kad `git push` bude odbijen (`! [rejected] ... fetch first`)

Znači da je neko drugi pushao na `origin/main` u međuvremenu, pa su grane **divergirale**.
**NE radi `git push --force`** — pregazio bi tuđi rad. Umjesto toga presloži svoj commit
na vrh udaljenog (rebase), pa pushaj.

Tačni koraci (isto kao što smo radili):

```bash
# 1. Povuci najnovije stanje sa servera (ne mijenja tvoju granu, samo origin/main)
git fetch origin

# 2. Vidi koliko je divergiralo  (left = samo na serveru, right = samo lokalno)
git rev-list --left-right --count origin/main...main

# 3. Vidi KOJI commiti
git log --oneline main..origin/main     # tuđi commiti koje nemaš
git log --oneline origin/main..main     # tvoji commiti koje server nema

# 4. Ako rebase javi "You have unstaged changes" — skloni ih privremeno.
#    Cijeli radni direktorij:
git stash push -m "wip prije push"
#    ...ili samo jedan fajl:
git stash push -m "wip" putanja/do/fajla

# 5. Presloži svoj(e) commit(e) na vrh servera
git rebase origin/main
#    Ako ima KONFLIKATA: otvori fajlove, riješi <<<<<<< ======= >>>>>>>, pa:
#       git add <fajl> ; git rebase --continue
#    Ako želiš odustati i vratiti na prije rebasea:
#       git rebase --abort

# 6. Push (sad je čist fast-forward)
git push origin main

# 7. Vrati ono što si stashovao u koraku 4
git stash pop
```

**Skraćeno** (ako nemaš neukomitovanih izmjena): `git pull --rebase origin main` pa `git push`.

Pravila:
- Nikad `--force` / `--force-with-lease` na `main` osim ako svi u timu znaju.
- Rebase koristi za **lokalne, još nepushane** commite — to je bezbjedno.
- Ako nisi siguran, prvo `git fetch` + `git log` da vidiš stanje prije bilo čega.

---

## 2. Okruženje — bitne začkoljice

### Frontend: NEMA lokalnih `node_modules`
`npm run lint` / `npm run build` iz hosta (PowerShell) **ne rade** — `eslint`/`vite` nisu
instalirani lokalno (`'eslint' is not recognized...`). Sve npm komande idu **unutar Docker
kontejnera**:

```bash
docker compose exec frontend npm run lint
docker compose exec frontend npm run build
```

(Frontend dev server ionako radi u kontejneru s Vite HMR-om — izmjene se vide odmah uz refresh.)

### Backend: `pytest` trenutno NE radi
`docker compose exec backend python -m pytest` pada u **setup fixture**, prije bilo kakvog
test koda:
```
asyncpg ... UndefinedObjectError: constraint "fk_status_agenta_eskalacija"
of relation "status_agenta" does not exist
```
To je problem test-harnessa/migracija oko **eskalacija** tabela (`status_agenta`, `eskalacija`),
**nije** znak da je feature kod pokvaren. Treba zasebno popraviti fixture/migracije.

Dok se to ne popravi, backend izmjene verifikuj ovako:
```bash
# da li se app uopšte učita (uhvati syntax/import greške)
docker compose exec backend python -c "from app.main import app; print('ok')"
# da li se konkretan modul importuje
docker compose exec backend python -c "import app.api.v1.routes.transcripts; print('ok')"
```

### Ostalo
- `docker-compose.yml: the attribute 'version' is obsolete` u outputu je benigno upozorenje
  (možeš ignorisati ili obrisati `version:` liniju iz compose fajlova).
- Komande se pokreću iz `projekat/` (gdje su compose fajlovi).
