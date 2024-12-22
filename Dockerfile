# Build stage
FROM python:3.9-slim as builder

# Systeem dependencies alleen voor build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Kopieer alleen requirements files eerst voor betere cache benutting
COPY requirements/base.txt requirements/base.txt
COPY requirements/api.txt requirements/api.txt

# Installeer dependencies in een virtuele omgeving
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Installeer dependencies met caching
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements/api.txt

# Download models naar een specifieke directory
RUN mkdir -p /app/models && \
    python -c "from transformers import AutoTokenizer, AutoModelForTokenClassification; \
    model_name='pdelobelle/robbert-v2-dutch-ner'; \
    AutoTokenizer.from_pretrained(model_name, cache_dir='/app/models'); \
    AutoModelForTokenClassification.from_pretrained(model_name, cache_dir='/app/models')"

# Runtime stage
FROM python:3.9-slim

# Kopieer alleen de virtuele omgeving van de builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Kopieer de gedownloade models
COPY --from=builder /app/models /app/models
ENV TRANSFORMERS_CACHE=/app/models

WORKDIR /app

# Kopieer applicatie code
COPY src/ src/
COPY main.py .

# Runtime configuratie
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start de applicatie
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]