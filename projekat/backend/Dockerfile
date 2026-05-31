# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

# No build toolchain needed: every dependency ships a manylinux wheel for CPython 3.12
# (psycopg2-binary and asyncpg bundle libpq; cryptography/bcrypt/spaCy/torch are all
# prebuilt). Dropping the old `apt-get install build-essential libpq-dev` layer removes
# a slow apt step and a few hundred MB from every cold build.

# 1) CPU-only torch first, in its own layer (sentence-transformers would otherwise pull
#    the multi-GB CUDA build). This app embeds on CPU, so the result is identical.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=100 torch --index-url https://download.pytorch.org/whl/cpu

# 2) Heavy, rarely-changing ML deps + the spaCy model, before the app-level deps — so
#    editing requirements.txt does not reinstall this multi-hundred-MB set.
COPY requirements-ml.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=100 -r requirements-ml.txt && \
    python -m spacy download xx_ent_wiki_sm

# 3) Remaining app dependencies (these change far more often). The pip cache mount keeps
#    downloaded wheels between builds, so a requirements.txt edit only fetches what changed.
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=100 -r requirements.txt

COPY . .

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
