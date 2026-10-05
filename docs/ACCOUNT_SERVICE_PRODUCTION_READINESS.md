# Account Service Production Readiness

This document tracks whether the Account Service is ready to support real GO Available mobile and web clients.

It is different from `PROGRESS.md`.

- `PROGRESS.md` explains daily learning progress and next moves.
- This file is the production readiness checklist for the Account Service.

## Readiness Summary

Current status:

```text
Not production-complete yet
```

The Account Service has a strong production foundation, but it still needs final auth hardening, deployment environment proof, monitoring decisions, and real load-test numbers before we call it done.

## Production Definition

The Account Service is production-ready when this flow is safe and verified:

```text
Mobile/Web client signs in with Supabase
-> Supabase returns a JWT
-> client sends Authorization: Bearer <jwt>
-> Account Service verifies the JWT
-> Account Service maps the Supabase user to a GO account
-> Account Service creates, reads, or updates allowed account fields
-> invalid or abusive requests are rejected
-> errors are logged and visible
-> CI checks the service before merge
-> hosted runtime can start through Gunicorn or Docker
-> baseline load-test numbers are recorded
```

Google and Apple login are client/Supabase responsibilities.

The backend responsibility is to trust only the Supabase-issued JWT and then apply GO Account business rules.

## Current Production Foundation

### Service Runtime

Status:

```text
Done
```

Evidence:

- `services/account/Dockerfile` builds the Account Service container.
- `docs/ACCOUNT_SERVICE_RUNTIME.md` documents Gunicorn and Docker runtime.
- GitHub Actions checks Gunicorn configuration.
- GitHub Actions builds the Account Service container.

Production expectation:

```zsh
cd services/account
python -m gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

### Database Configuration

Status:

```text
Done for configuration, not yet proven on hosted production database
```

Evidence:

- `DATABASE_URL` is required.
- Django uses `dj-database-url`.
- Database connections use persistent connections and health checks.
- CI runs against PostgreSQL.

Remaining proof:

- run migrations against the real hosted Account database
- verify `/api/v1/ready` against the hosted database

### Account API Behavior

Status:

```text
Mostly done
```

Current endpoints:

```text
GET /api/v1/health
GET /api/v1/ready
POST /api/v1/account
GET /api/v1/account/me
PATCH /api/v1/account/me
```

Current behavior:

- creates accounts for authenticated identities
- reads the current user's account
- updates safe profile fields
- protects stable identity fields
- validates username behavior
- uses stable `user_id` and `supabase_user_id`

Remaining proof:

- final auth-hardening tests before mobile integration
- hosted smoke test after deployment

### Authentication

Status:

```text
In progress
```

Current foundation:

- Bearer JWT parsing exists.
- Supabase JWT secret, audience, and issuer settings exist.
- Dev auth header is disabled by default.
- CI sets `ALLOW_DEV_AUTH_HEADER=false`.

Production requirement:

```text
Authorization: Bearer <supabase-jwt>
```

The dev-only header:

```text
X-Supabase-User-Id
```

must never be usable accidentally in production.

Next branch goal:

```text
backend/account-supabase-auth-hardening
```

Required tests:

- missing token is rejected
- malformed token is rejected
- invalid signature is rejected
- valid token is accepted
- dev header works only when explicitly enabled
- dev header is rejected when disabled

### Security Settings

Status:

```text
Mostly done
```

Current foundation:

- `DJANGO_SECRET_KEY` is required.
- `DJANGO_DEBUG` defaults to false.
- `DJANGO_ALLOWED_HOSTS` is environment-controlled.
- secure cookies default to production-safe values when debug is false.
- `X_FRAME_OPTIONS` is denied.
- content type sniffing protection is enabled.
- proxy SSL header support is opt-in.
- API docs are controlled by `ENABLE_API_DOCS`.

Remaining proof:

- verify production environment variables on the real host
- verify API docs are disabled or intentionally protected in production
- verify HTTPS/proxy settings against the chosen host

### Rate Limiting

Status:

```text
Done for first Account endpoints
```

Current limits:

```text
ACCOUNT_CREATE_THROTTLE_RATE=5/minute
ACCOUNT_UPDATE_THROTTLE_RATE=10/minute
```

Current protected operations:

- account creation
- profile update

Remaining proof:

- adjust limits after real mobile usage and load-test results

### Logging

Status:

```text
Done for structured console logging
```

Current foundation:

- logs include timestamp, level, logger, and message
- `django` logger is configured
- `api` logger is configured
- log level is controlled by `DJANGO_LOG_LEVEL`

Remaining proof:

- confirm hosted platform captures stdout/stderr logs
- decide whether Sentry is added now or after first deployment

### Monitoring and Error Reporting

Status:

```text
Not done yet
```

Production expectation:

- server errors should be visible without reading raw terminal output
- deploys should make it obvious when Account Service breaks

Options:

- add Sentry during Account production finish
- postpone Sentry but record it as a required pre-launch item

Decision needed:

```text
Add Sentry now or explicitly defer it.
```

### CI

Status:

```text
Done and improving
```

Current CI responsibilities:

- install pinned dependencies
- run Black check
- run Django system check
- check Gunicorn config
- build Account Service Docker image
- check migrations
- validate OpenAPI schema
- run tests
- use PostgreSQL service

Remaining improvement:

- ensure auth-hardening tests are part of the normal test suite
- keep CI as the merge gate for Account Service branches

### Deployment Environment

Status:

```text
Not hosted yet
```

Required production variables:

```text
DJANGO_SECRET_KEY
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS
DJANGO_CSRF_TRUSTED_ORIGINS
DATABASE_URL
SUPABASE_JWT_SECRET
SUPABASE_JWT_AUDIENCE
SUPABASE_JWT_ISSUER
ALLOW_DEV_AUTH_HEADER=false
ENABLE_API_DOCS=false
ACCOUNT_CREATE_THROTTLE_RATE
ACCOUNT_UPDATE_THROTTLE_RATE
DJANGO_LOG_LEVEL
```

Host-specific variables may also be needed:

```text
PORT
DJANGO_SECURE_SSL_REDIRECT
DJANGO_SESSION_COOKIE_SECURE
DJANGO_CSRF_COOKIE_SECURE
DJANGO_TRUST_PROXY_SSL_HEADER
```

Deployment is ready to attempt only after auth hardening is merged.

### Load Testing

Status:

```text
Not done yet
```

Do not claim support for 500K users yet.

Required baseline endpoints:

```text
GET /api/v1/health
GET /api/v1/ready
POST /api/v1/account
GET /api/v1/account/me
PATCH /api/v1/account/me
```

Record:

- test environment
- command/tool used
- total requests
- requests per second
- p50 latency
- p95 latency
- p99 latency
- error rate
- database behavior

Acceptable first goal:

```text
Baseline numbers recorded with honest limits.
```

Not acceptable:

```text
Claiming large-scale readiness without measurements.
```

## Final Account Backend Gate

Account backend can be called foundation-complete when all of these are true:

- production-runtime PR is merged
- Supabase auth-hardening PR is merged
- dev auth fallback cannot be used accidentally in production
- Account tests pass
- migration check passes
- schema validation passes
- Black check passes
- Gunicorn config check passes
- Docker build passes in CI
- required production environment variables are documented
- hosted smoke test passes, or hosting is explicitly scheduled as the next gate
- monitoring decision is recorded
- baseline load-test result is recorded

## Next Move

Current branch:

```text
backend/account-supabase-auth-hardening
```

Next production slice:

```text
Harden Account Service Supabase auth
```

Primary files:

```text
services/account/api/auth.py
services/account/api/tests/test_auth.py
services/account/config/settings.py
services/account/.env.example
```

Primary learning goal:

Explain how this flow works:

```text
Supabase login
-> JWT
-> Authorization header
-> Django auth parser
-> Supabase user id
-> GO account
-> response to mobile/web
```
