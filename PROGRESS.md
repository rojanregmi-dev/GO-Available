# GO A Progress

## 2026-10-05 - Account Service Production Finish Plan

### Project Direction

GO A is the production-level rebuild of GO AVI.

GO AVI remains the reference project. GO A is where we rebuild the backend with cleaner service boundaries, stronger security, real CI, production runtime, and measurable checks.

The current focus is not the whole GO Available app. The current focus is finishing the Account Service backend so mobile and web clients can safely use it.

### Production Rules

- Keep `main` clean.
- Use one focused feature branch per production slice.
- Use Django and Django REST Framework for backend services.
- Use Supabase Auth for real user authentication.
- Do not commit secrets, local `.env` files, virtual environments, databases, or caches.
- Do not claim scale such as 500K users until load tests produce real numbers.
- Every production slice should have:
  - clear behavior
  - tests when behavior changes
  - Black formatting
  - Django checks
  - migration checks
  - CI verification
  - a focused commit and PR

### Current Live State

Current working branch:

```text
backend/account-supabase-auth-hardening
```

Current `main` includes the production runtime merge:

```text
53b171c Merge pull request #22 from rojanregmi-dev/backend/account-production-runtime
```

The Account Service now has production runtime support merged into `main`.

### What Account Service Can Do Now

The Account Service can currently:

- start as a Django service under `services/account`
- connect through `DATABASE_URL`
- expose health and readiness endpoints
- create an account for an authenticated identity
- return the current user's account
- update safe profile fields
- protect account APIs with the auth layer
- keep stable identity fields separate from editable public profile fields
- generate stable user numbers
- validate username behavior
- generate API docs when docs are enabled
- run Black formatting checks
- run Django checks and tests in CI
- use production security settings
- use structured logging
- rate limit account creation and profile updates
- run through Gunicorn instead of Django `runserver`
- build an Account Service Docker image

### What "Account Backend Done" Means

Account backend is considered done when this flow works safely:

```text
Mobile/Web user signs in with Supabase
-> Supabase returns a JWT
-> client sends Authorization: Bearer <jwt> to Django
-> Account Service verifies the JWT
-> Account Service identifies the stable Supabase user
-> Account Service creates/reads/updates the GO account
-> unsafe requests are rejected
-> abuse is rate limited
-> errors are visible through logs/monitoring
-> service can run in production through Gunicorn/Docker
-> CI proves the behavior before merge
```

Google and Apple login buttons are mostly mobile/Supabase client work.

Django's backend responsibility is to correctly trust the Supabase JWT that Google or Apple login produces.

### Current Gap

The Account Service has the foundation for Supabase JWT auth, but this next branch must harden the production auth boundary.

The important remaining Account backend questions are:

- Is dev auth fallback impossible to use accidentally in production?
- Do tests prove missing, bad, and valid auth behavior?
- Are Supabase auth settings documented clearly for a real project?
- Can mobile/web safely call Account APIs after Supabase login?
- Is deployment configuration clear enough for a real host?
- Do we have monitoring/error reporting or a clear decision to postpone it?
- Do we have baseline load-test numbers instead of guesses?

### Four-Day Account Backend Finish Plan

#### Day 1 - Supabase Auth Hardening

Goal:

Make real Supabase JWT auth the production path and make dev auth clearly local-only.

Work:

- inspect `services/account/api/auth.py`
- inspect account endpoint tests
- tighten `ALLOW_DEV_AUTH_HEADER` behavior
- document real Supabase JWT environment variables
- ensure CI uses production-style auth defaults

Expected result:

The service is clearly moving from "temporary development badge" to "real Supabase badge scanner."

#### Day 2 - Auth Test Coverage

Goal:

Prove the Account Service accepts only the right identity path.

Work:

- test missing token is rejected
- test invalid token is rejected
- test valid JWT is accepted
- test dev header works only when explicitly enabled
- test dev header is rejected when disabled
- run full Account Service test suite

Expected result:

We can explain and prove the auth boundary before connecting the mobile app.

#### Day 3 - Deployment Environment and Monitoring

Goal:

Make the Account Service ready for a real hosted environment.

Work:

- finalize required environment variables
- verify Gunicorn runtime docs
- verify Docker runtime docs
- decide whether Sentry is added now or tracked as a next production task
- update README/runtime docs if needed

Expected result:

A host can run the Account Service without guessing which variables or commands are required.

#### Day 4 - Load Test Baseline and Final Account Review

Goal:

Get honest baseline numbers for Account endpoints and close the Account backend foundation.

Work:

- add or run load-test commands against Account endpoints
- record request rate, latency, and error rate
- update docs with actual numbers
- update this progress file
- prepare final Account backend cleanup PR

Expected result:

We can say what Account Service actually handled, not what we hope it can handle.

### Next Immediate Step

Work on the current branch:

```text
backend/account-supabase-auth-hardening
```

First code target:

```text
services/account/api/auth.py
services/account/api/tests/test_auth.py
services/account/.env.example
services/account/config/settings.py
```

First behavior target:

```text
Dev auth header must be local-only.
Production auth must depend on Supabase Bearer JWT.
Tests must prove both paths.
```

### Checks To Run For The Next Account Auth PR

From the repository root:

```zsh
./.venv/bin/python -m black --check services/account
cd services/account
../../.venv/bin/python manage.py check
../../.venv/bin/python manage.py makemigrations --check --dry-run
../../.venv/bin/python manage.py spectacular --file /tmp/account-schema.yml --validate
../../.venv/bin/python manage.py test
cd ../..
git diff --check
```

If auth behavior changes, the most important test file is:

```text
services/account/api/tests/test_auth.py
```

### Current Understanding To Review

Before moving beyond Account auth, the developer should be able to explain:

- why Django should not implement Google/Apple OAuth directly here
- why Supabase returns the JWT
- why the mobile app sends `Authorization: Bearer <jwt>`
- why Django verifies that token before touching account data
- why `user_id` and `supabase_user_id` are stable backend identity fields
- why username/display name are editable public profile fields
- why dev auth fallback must not be available in production

### Commit Status

Production runtime has already been merged into `main`.

Current auth-hardening branch is not committed yet in this progress entry.

Next meaningful commit should be something like:

```text
Harden Account Service Supabase auth
```

Only commit after the auth changes and checks are complete.
