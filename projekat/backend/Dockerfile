# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

# No build toolchain needed: every dependency ships a manylinux wheel for CPython 3.12
# (psycopg2-binary and asyncpg bundle libpq; cryptography/bcrypt/spaCy/torch are all
# prebuilt). Dropping the old `apt-get install build-essential libpq-dev` layer removes
# a slow apt step and a few hundred MB from every cold build.

# 1) CPU-only torch first, in its own layer (sentence-transformers would otherwise pull
#    the multi-GB CUDA build). This app embeds on CPU, so the result is identical, and
#    torch is satisfied before the resolve below so it's never re-touched.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=100 torch --index-url https://download.pytorch.org/whl/cpu

# 2) All Python deps in ONE resolve. Installing requirements in a single pass lets pip
#    pick the pinned versions directly — no install-then-downgrade churn and minimal
#    backtracking (the langchain transitive deps are pinned in requirements.txt for the
#    same reason). The BuildKit cache mount keeps downloaded wheels between builds, so a
#    requirements edit only re-fetches what changed.
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=100 -r requirements.txt && \
    python -m spacy download xx_ent_wiki_sm

COPY . .

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
