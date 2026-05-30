# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

# System dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install CPU-only torch first so sentence-transformers does not pull the
# multi-GB CUDA/NVIDIA build. This app runs embeddings on CPU only, so the
# resulting environment is identical to before, just far smaller and faster.
# Kept in its own layer so it stays cached across requirements.txt changes.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=100 torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
# Cache mount keeps downloaded wheels between builds, so editing requirements.txt
# only re-downloads the packages that actually changed.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=100 -r requirements.txt && \
    python -m spacy download xx_ent_wiki_sm

COPY . .

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
