# GO A 4-Month Production Roadmap

This document explains what we have already built, what we still need to build, what system design we are following, what tools we will use, and what can realistically be completed in 4 months.

This is not a pass/fail readiness checklist.

This is the step-by-step production roadmap for building GO Available like a real software engineering project.

## Product Goal

GO Available is a mobile-first social coordination app.

The backend must support:

- mobile app first
- future web app using the same APIs
- real user authentication
- account/profile identity
- discovery/map/feed behavior
- social relationships
- messaging
- production deployment
- measurable performance checks

GO AVI is the reference project. GO A is the cleaner production rebuild.

We do not blindly copy GO AVI. For each feature, we inspect the matching GO AVI behavior, understand the dependency chain, then rebuild it with a stronger Django/service design.

## Current Status

Current active branch:

```text
backend/account-supabase-auth-hardening
```

Latest completed foundation:

```text
Account Service production runtime is merged into main.
```

The project is currently in the Account backend finishing phase.

The whole app is not complete yet. The Account Service is the first real production service.

## What We Have Done So Far

### Repository and Workflow

Done:

- created the GO A repository
- created a `main` branch workflow
- use focused feature branches
- use PR-style development
- use meaningful commits per production slice
- added GitHub Actions CI for Account Service
- added Black formatting checks
- added Django checks
- added migration checks
- added test suite checks
- added schema validation checks
- added Gunicorn runtime check
- added Docker build check

Why this matters:

This makes GO A feel like a real engineering project, not random local code.

### Account Service Foundation

Done:

- created `services/account`
- created Django project and API app
- added Django REST Framework
- added Account model
- added stable account identity fields
- added account creation service
- added account update service
- added serializers
- added migrations
- added tests

Current Account identity rules:

```text
user_id          = stable internal GO account id
supabase_user_id = stable Supabase auth user id
user_number      = stable public account number
username         = public handle, can change
display_name     = public display name, can change
```

Why this matters:

Other services must depend on stable identity, not username. Username can change, but `user_id` and `supabase_user_id` must remain stable.

### Account APIs

Done:

```text
GET /api/v1/health
GET /api/v1/ready
POST /api/v1/account
GET /api/v1/account/me
PATCH /api/v1/account/me
```

Current behavior:

- health endpoint proves the service is alive
- readiness endpoint checks database readiness
- create account endpoint creates or returns the user's account
- me endpoint returns the current user's account
- update endpoint edits safe profile fields
- protected identity fields are not editable through profile update

Why this matters:

This is the Account Service front office. Before Discovery, Social, or Messaging exists, every real user needs a stable account identity.

### Authentication Foundation

Done:

- added Supabase JWT auth foundation
- added Bearer token parsing
- added Supabase JWT settings
- added dev auth fallback for local development
- made dev auth disabled by default

In progress:

- harden production auth behavior
- prove dev auth cannot be used accidentally in production
- expand auth tests

Why this matters:

Google and Apple login happen through Supabase on the client side. Django should not own Google or Apple OAuth directly. Django should verify the Supabase JWT and then apply GO Account rules.

### Production Settings

Done:

- `DJANGO_SECRET_KEY` is required
- `DJANGO_DEBUG` defaults to false
- `DJANGO_ALLOWED_HOSTS` is environment-controlled
- `DATABASE_URL` is required
- production cookie/security settings exist
- API docs are controlled by `ENABLE_API_DOCS`
- proxy HTTPS support is configurable

Why this matters:

Production apps must not depend on local defaults or hidden config.

### Runtime and Deployment Foundation

Done:

- added Gunicorn
- documented production start command
- added Dockerfile
- added `.dockerignore`
- added CI Docker build check
- added Account runtime documentation

Production start command:

```zsh
cd services/account
python -m gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Why this matters:

Django `runserver` is for local development. Production needs Gunicorn or container runtime.

### Logging and Rate Limits

Done:

- added structured console logging
- added configurable log level
- added account creation rate limit
- added account update rate limit
- added tests for rate limiting

Why this matters:

Logs help us see production behavior. Rate limits help stop abuse before it becomes expensive or dangerous.

## What We Have Not Done Yet

Not done yet:

- real Supabase project values connected
- real Google login from mobile
- real Apple login from mobile
- final auth hardening tests
- real hosted deployment
- Sentry/error monitoring
- load tests with real numbers
- Discovery Service
- Social Service
- Messaging Service
- API Gateway or routing layer
- Redis/cache
- background workers
- mobile app integration with the new backend
- web app

This is normal. We are building foundation first.

## System Design We Are Using

### High-Level Architecture

```text
Mobile App / Future Web App
        |
        v
Supabase Auth
        |
        v
Authorization: Bearer <jwt>
        |
        v
API Gateway / Load Balancer
        |
        v
Backend Services
  - Account Service    -> Account PostgreSQL
  - Discovery Service  -> Discovery PostgreSQL
  - Social Service     -> Social PostgreSQL
  - Messaging Service  -> Messaging PostgreSQL
        |
        v
Redis / Cache
        |
        v
Queue / Workers
        |
        v
Logs / Metrics / Sentry / Tracing
```

### Service Ownership

Each service owns its own data.

```text
Account Service
  owns accounts, profiles, stable user identity

Discovery Service
  owns location, radius, nearby users, feed/map/list discovery

Social Service
  owns follows, friends, blocks, privacy rules

Messaging Service
  owns conversations, messages, delivery/read state
```

Rules:

- no service directly writes another service's database
- no cross-database foreign keys
- use stable IDs between services
- use versioned APIs
- add events later only when needed

### Request Flow Example

For account profile:

```text
User opens app
-> mobile app has Supabase session
-> mobile app sends GET /api/v1/account/me
-> request includes Authorization: Bearer <jwt>
-> Django verifies JWT
-> Django extracts Supabase user id
-> Account Service finds matching GO account
-> Account Service serializes account response
-> mobile app updates profile screen
```

### Why This Design

We are using this design because it gives us:

- clear ownership
- cleaner testing
- safer scaling path
- easier future web support
- real production deployment path
- better interview story
- less messy coupling than the original reference app

## What We Will Use

### Backend

- Python
- Django
- Django REST Framework
- PostgreSQL
- Supabase Auth
- PyJWT
- Gunicorn
- Docker
- GitHub Actions
- Black
- drf-spectacular for OpenAPI docs

### Production and Operations

- hosted PostgreSQL
- container or Python web service host
- environment variables for config
- Sentry for error monitoring, if we choose to add it now
- logs through stdout/stderr
- load testing tool to record real numbers

### Future Supporting Infrastructure

Use only when the app needs it:

- Redis for caching, throttling, presence, or hot reads
- background workers for slow jobs
- queue for notifications and fanout
- API gateway/load balancer for service routing
- object storage for media later

## Step-by-Step Build Plan

## Month 1 - Finish Account Backend

Goal:

Finish Account Service as the first production backend service.

Steps:

1. Harden Supabase JWT auth.
2. Prove dev auth fallback is local-only.
3. Add missing auth tests.
4. Connect real Supabase project settings.
5. Document mobile Google/Apple auth flow.
6. Prepare real deployment environment variables.
7. Add or decide on Sentry.
8. Run baseline Account endpoint load tests.
9. Update docs with real results.

Month 1 result:

```text
Account Service backend foundation complete.
```

What "complete" means here:

- account APIs work
- real auth boundary is proven
- CI passes
- production runtime exists
- deployment configuration is clear
- load-test baseline exists

## Month 2 - Build Discovery Service

Goal:

Build the service that powers nearby/map/feed behavior.

Steps:

1. Inspect GO AVI discovery/map/feed behavior.
2. Create `services/discovery`.
3. Add Discovery database config.
4. Design location model.
5. Design availability/radius model.
6. Add create/update location endpoint.
7. Add nearby discovery endpoint.
8. Add feed/list endpoint.
9. Add basic geo query strategy.
10. Add tests.
11. Add API docs.
12. Add CI support.

Month 2 result:

```text
Users can have account identity and discover nearby available people.
```

Important design point:

Discovery Service references Account users by stable `user_id`. It does not own profile identity.

## Month 3 - Build Social and Messaging Foundations

Goal:

Build the relationship and communication layer.

Social steps:

1. Inspect GO AVI relationship behavior.
2. Create `services/social`.
3. Add follow/friend/block models.
4. Add privacy rules.
5. Add relationship endpoints.
6. Add tests and docs.

Messaging steps:

1. Inspect GO AVI messaging behavior.
2. Create `services/messaging`.
3. Add conversation model.
4. Add message model.
5. Add send/list message endpoints.
6. Add read/delivery state foundation.
7. Add tests and docs.

Month 3 result:

```text
Users can discover, connect, and message through backend APIs.
```

Important design point:

Messaging should not directly own account profile data. It stores participant IDs and asks Account/Social rules when needed.

## Month 4 - Integration, Deployment, and Scale Proof

Goal:

Turn the backend services into a usable MVP foundation.

Steps:

1. Connect mobile app to Supabase Auth.
2. Connect mobile app to Account APIs.
3. Connect mobile app to Discovery APIs.
4. Connect mobile app to Social APIs.
5. Connect mobile app to Messaging APIs.
6. Deploy backend services.
7. Configure production env vars.
8. Add Sentry/error monitoring if not already added.
9. Add smoke tests.
10. Add load-test scripts.
11. Run baseline load tests.
12. Fix bottlenecks found by testing.
13. Update documentation with real numbers.

Month 4 result:

```text
GO Available has a production-style backend MVP connected to mobile.
```

## What Can Realistically Be Complete In 4 Months

Realistic 4-month complete target:

- Account Service production foundation
- Discovery Service foundation
- Social Service foundation
- Messaging Service foundation
- Supabase Auth integration
- mobile app connected to backend APIs
- production deployment path
- CI for backend services
- tests for core behavior
- Sentry or documented monitoring decision
- baseline load-test numbers
- clear technical documentation

Not realistic in 4 months unless we cut quality:

- proving 500K-user support
- perfect large-scale distributed system
- advanced recommendation engine
- complex real-time messaging infrastructure
- polished web app and mobile app at the same time
- every edge case from a mature social platform

Senior-engineer answer:

```text
In 4 months, we can build a real production-style MVP foundation.
We cannot honestly claim massive scale until deployment and load testing prove it.
```

## Daily Working Method

Each workday should follow this loop:

1. Check current branch and status.
2. Read the relevant roadmap/progress section.
3. Pick one small production behavior.
4. Inspect GO AVI reference for matching behavior if applicable.
5. Explain the behavior before coding.
6. Add one manageable code slice.
7. Run focused checks.
8. Review the diff.
9. Update docs if the system changed.
10. Commit one meaningful slice when checks pass.

## Next Immediate Work

Current phase:

```text
Month 1 - Finish Account Backend
```

Current branch:

```text
backend/account-supabase-auth-hardening
```

Next behavior:

```text
Production auth must depend on Supabase Bearer JWT.
Dev auth fallback must remain local-only.
Tests must prove both paths.
```

Primary files:

```text
services/account/api/auth.py
services/account/api/tests/test_auth.py
services/account/config/settings.py
services/account/.env.example
```

Expected commit:

```text
Harden Account Service Supabase auth
```
