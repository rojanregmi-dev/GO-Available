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

## Supabase Authentication Smoke Test

After creating or signing in a test user through Supabase, keep the access token
out of source control and out of chat. Store it only in the current terminal:

```zsh
cd services/account
read -s SUPABASE_SMOKE_TEST_TOKEN
export SUPABASE_SMOKE_TEST_TOKEN
../../.venv/bin/python scripts/account_auth_smoke_test.py
unset SUPABASE_SMOKE_TEST_TOKEN
```

The smoke test calls `GET /api/v1/account/me`. A `200` means the token
identified an existing GO account. A `404` means Supabase authentication
succeeded but the GO account profile does not exist yet. A `401` means Django
rejected the token.

Use `ACCOUNT_API_URL` when testing a hosted Account Service instead of the
default local URL:

```zsh
ACCOUNT_API_URL=https://api.example.com/api/v1/account/me \
  ../../.venv/bin/python scripts/account_auth_smoke_test.py
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
SUPABASE_URL
SUPABASE_JWT_AUDIENCE
```

Set `SUPABASE_URL` to the project's origin, for example
`https://<project-ref>.supabase.co`. Django derives the JWT issuer and JWKS
endpoint from this single value. Production requires HTTPS. The Account Service
does not need a Supabase secret or service-role API key to verify user JWTs.

## Container Runtime

The Account Service has a Dockerfile for hosts that deploy containers:

```zsh
docker build -f services/account/Dockerfile .
```

The image:

- installs pinned Python dependencies from `requirements.txt`
- copies only the Account Service source into the runtime image
- runs as a non-root `appuser`
- starts Gunicorn with the host-provided `PORT`

The `.dockerignore` file keeps local secrets, virtual environments, Python caches, and SQLite databases out of the image.

The health endpoints have different jobs:

- `/api/v1/health` confirms that the web process is responding.
- `/api/v1/ready` runs a small database query and returns `503` when the Account database is unavailable.

A hosting platform should send traffic to the Account Service only after the readiness endpoint reports `200`.

If PostgreSQL becomes temporarily unavailable during an authenticated Account request, the API returns `503` with a `Retry-After: 5` header and logs the failure. Clients should retry that response rather than treating it as a permanent account error.

If the Supabase JWKS endpoint is unreachable when a signing key must be fetched,
the API also returns `503` with `Retry-After: 5`. A malformed or invalid JWT
still returns `401`. The JWKS set is cached by the verifier for five minutes,
and its outbound request times out after five seconds.

## CI Runtime Check

GitHub Actions verifies that Gunicorn can load the Account Service WSGI app:

```zsh
python -m gunicorn --check-config config.wsgi:application
```

This does not start a public server. It checks that production runtime configuration can be imported successfully.

GitHub Actions also builds the Account Service container to catch Dockerfile or dependency problems before merge.
After the build, CI starts the container with production-style environment variables and requests both `/api/v1/health` and `/api/v1/ready`. This catches runtime startup failures that an image build alone cannot detect.
