FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src ./src
COPY api ./api

RUN pip install --upgrade pip && pip install ".[api]"

EXPOSE 8000
# Note: this image runs the CPU fast-path API. A GPU image for scVI training
# would extend a CUDA base and install ".[scvi]".
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
