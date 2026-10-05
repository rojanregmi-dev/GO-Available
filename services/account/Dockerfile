FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

RUN useradd --create-home --shell /usr/sbin/nologin appuser

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser services/account ./services/account

USER appuser
WORKDIR /app/services/account

EXPOSE 8000

CMD ["sh", "-c", "python -m gunicorn config.wsgi:application --bind 0.0.0.0:${PORT}"]
