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
COPY setup.py .

# Installeer dependencies in een virtuele omgeving
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set environment variables for model caching
ENV TRANSFORMERS_CACHE=/app/models
ENV HF_HOME=/app/models
ENV TORCH_HOME=/app/models

# Installeer dependencies met caching
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements/api.txt

# Download models naar een specifieke directory
RUN mkdir -p /app/models && \
    python -c "from transformers import AutoTokenizer, AutoModelForTokenClassification; \
    model_name='pdelobelle/robbert-v2-dutch-ner'; \
    AutoTokenizer.from_pretrained(model_name, cache_dir='/app/models'); \
    AutoModelForTokenClassification.from_pretrained(model_name, cache_dir='/app/models')" && \
    chmod -R 777 /app/models

# Create storage directory with correct permissions
RUN mkdir -p /app/storage/processed && \
    chmod -R 777 /app/storage

# Runtime stage
FROM python:3.9-slim

# Installeer Tesseract OCR en Nederlandse taaldata
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-nld \
    poppler-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Kopieer alleen de virtuele omgeving van de builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set environment variables for model caching and disable torch dynamo
ENV TRANSFORMERS_CACHE=/app/models
ENV HF_HOME=/app/models
ENV TORCH_HOME=/app/models
ENV PYTHONUNBUFFERED=1
ENV TORCHDYNAMO_DISABLE=1

# Kopieer de gedownloade models met juiste permissions
COPY --from=builder /app/models /app/models
RUN chmod -R 777 /app/models

# Create storage directory with correct permissions
RUN mkdir -p /app/storage && \
    chmod -R 777 /app/storage && \
    chown -R 1000:1000 /app/storage /app/models

WORKDIR /app

# Kopieer alleen de benodigde applicatie code
COPY src/ src/
COPY main.py .
COPY setup.py .

# Installeer package in development mode
RUN pip install -e .

EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Set user
USER 1000

# Start de applicatie
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8080"]