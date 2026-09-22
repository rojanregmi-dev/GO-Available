# GO A Progress

## 2026-09-21

### What We Decided

- GO A is the new production-level app, not a simple learning clone.
- GO avi is the main reference for security, backend behavior, and load-tested engineering patterns.
- The backend must serve both the mobile app and the future web app.
- Mobile app comes first.
- We will use Django for backend services.
- We will use Supabase Auth for authentication.
- The first service ownership model is Account, Discovery, Social, and Messaging.
- Community is intentionally not part of the first build. It can become its own service later if the product needs it.

### What We Built

- Initialized a new Git repository on `main`.
- Created a local Python virtual environment at `.venv`.
- Installed Django and Django REST Framework.
- Created the first Django project skeleton for the Account Service.
- Moved the Django skeleton into `services/account/` so the repository can grow as a microservice-style backend.
- Added dependency tracking with `requirements.txt`.

### Current App Ability

The app has a Django project skeleton. It does not have GO business behavior yet.

Current service layout:

```text
services/
├── account/
│   ├── manage.py
│   ├── config/
│   └── api/
README.md
PROGRESS.md
requirements.txt
.gitignore
```

Runnable service today:

```text
services/account/
    ├── manage.py
    ├── config/
    └── api/
```

### Next Step

Add the first Account Service API endpoint:

```text
GET /api/v1/health
```

This will prove the backend can boot and answer a simple API request before we add databases, auth, or microservice complexity.

### Commit

Not committed yet.
