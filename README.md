# GO A

GO A is the production rebuild of GO, using lessons from GO avi as the main reference for security, backend behavior, and load-tested patterns.

## Product Direction

- Mobile app first.
- Web app later uses the same backend APIs.
- Supabase Auth proves who the user is.
- Django services own GO business logic and data.
- Each service owns its own PostgreSQL database.

## Service Ownership

```text
GO A
├── Account Service
│   └── Account PostgreSQL
├── Discovery Service
│   └── Discovery PostgreSQL
├── Social Service
│   └── Social PostgreSQL
└── Messaging Service
    └── Messaging PostgreSQL
```

No service reads or writes another service's database directly.

Account is the first service we are building. Discovery, Social, and Messaging are planned boundaries that we will add deliberately when we are ready.

## Identity Rule

- `user_id`: internal stable UUID, never changes.
- `user_number`: stable public account number, never changes.
- `username`: public handle like Instagram, can change.
- `display_name`: visible name, can change.

Relationships, messages, ownership, blocks, and service records must use stable identity, not username.

## Current Stack

- Python 3.10.6 locally
- Django 5.2
- Django REST Framework
- PostgreSQL planned per service
- Supabase Auth planned for authentication

## First Foundation Goal

Create the Django foundation inside `services/account/`, then add the first Account Service health endpoint:

```text
GET /api/v1/health
```

After that, add readiness checks, environment config, PostgreSQL, migrations, and Supabase JWT verification.
