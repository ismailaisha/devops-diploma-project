# ── Стадия 1: Builder ──────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Устанавливаем системные зависимости для сборки
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements первым — Docker кэширует этот слой
# Если requirements.txt не менялся — pip install не запускается заново
COPY requirements.txt .

# Устанавливаем зависимости в отдельную папку /install
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Стадия 2: Runtime ──────────────────────────────
FROM python:3.12-slim AS runtime

WORKDIR /app

# Только runtime зависимости — без gcc и build tools
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем установленные библиотеки из builder
COPY --from=builder /install /usr/local

# Копируем код приложения
COPY . .

# Создаём непривилегированного пользователя
# Запускать от root опасно — если взломают контейнер
# получат root доступ к системе
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Healthcheck — Docker проверяет что API живой
# Если /health не отвечает 3 раза — контейнер перезапускается
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]