# =============================================
# Multi-stage Dockerfile для Mesto Backend (FastAPI)
# =============================================

# ---------- Stage 1: builder ----------
# Устанавливаем зависимости в отдельном слое
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2: production ----------
# Финальный легковесный образ
FROM python:3.11-slim AS production

# Метаданные
LABEL maintainer="mesto-team" \
      description="Mesto Tour Booking API" \
      version="1.0"

# Создаём непривилегированного пользователя
RUN groupadd -r mesto && useradd -r -g mesto mesto

WORKDIR /app

# Копируем только установленные пакеты из builder-стадии
COPY --from=builder /install /usr/local

# Копируем код приложения
COPY . .

# Переключаемся на непривилегированного пользователя
USER mesto

EXPOSE 8000

# Healthcheck — Docker сам проверяет работоспособность контейнера
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
