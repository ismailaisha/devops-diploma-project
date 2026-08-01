# ── Стадия 1: Builder ──────────────────────────────
FROM python:3.12-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Стадия 2: Runtime ──────────────────────────────
FROM python:3.12-slim AS runtime
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 1. Создаем пользователя ЗАРАНЕЕ (слой закэшируется и не будет пересобираться)
RUN useradd -m -u 1000 appuser

# 2. Копируем библиотеки из билдера
COPY --from=builder /install /usr/local

# 3. Копируем код приложения, сразу назначая владельца appuser (избавляет от долгого chown)
COPY --chown=appuser:appuser . .

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
