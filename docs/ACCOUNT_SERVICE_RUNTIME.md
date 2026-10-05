# Account Service Runtime

This document explains how the Account Service runs in local development, CI, and future production hosting.

## Why Gunicorn

Django's `runserver` command is for local development only. A hosted backend needs a production WSGI server.

Gunicorn is the first production runtime for the Account Service.

## Local Development

Use Django management commands from the Account Service directory:

```zsh
cd services/account
../../.venv/bin/python manage.py check
../../.venv/bin/python manage.py test
```

For local browser/API testing, Django's development server is still fine:

```zsh
cd services/account
../../.venv/bin/python manage.py runserver 127.0.0.1:8000
```

## Production Start Command

Production hosting should run the WSGI app through Gunicorn:

```zsh
cd services/account
python -m gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

The host must provide environment variables such as:

```text
DJANGO_SECRET_KEY
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS
DATABASE_URL
SUPABASE_JWT_SECRET
SUPABASE_JWT_AUDIENCE
```

## CI Runtime Check

GitHub Actions verifies that Gunicorn can load the Account Service WSGI app:

```zsh
python -m gunicorn --check-config config.wsgi:application
```

This does not start a public server. It checks that production runtime configuration can be imported successfully.
