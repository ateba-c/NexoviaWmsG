# App Running Instructions

## Current State

The repository currently supports:

- backend code compilation
- frontend production build
- OpenAI-backed AI copilot endpoint wiring

Full database-backed testing and live API usage still depend on a working PostgreSQL instance and Redis.

## 1. Prerequisites

Install locally:

- Python 3.13 or a compatible project Python
- Node.js 20+
- PostgreSQL 16
- Redis

Use `.env.example` as the reference for local configuration.

Do not rely on the current `.env` contents when reviewing this repo state.

## 2. Backend Setup

From the repo root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements\development.txt
```

If you prefer to install the base requirements directly:

```powershell
python -m pip install -r requirements\base.txt
```

The OpenAI SDK is now included in `backend/requirements/base.txt`.

## 3. Frontend Setup

In a separate terminal:

```powershell
cd frontend
cmd /c npm install
```

## 4. Configure Environment

Copy values from `.env.example` into your own local environment setup.

Important variables for the AI copilot:

- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `OPENAI_SYSTEM_PROMPT`

Suggested minimum:

```text
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5
OPENAI_SYSTEM_PROMPT=You are the NexoFlow warehouse copilot. Provide concise warehouse operations guidance.
```

## 5. Start Infrastructure

If you are using local services directly, make sure PostgreSQL and Redis are running.

If you are using the Docker scaffolding, start the infra from:

- `infrastructure/docker/docker-compose.yml`

Then continue with Django migrations.

## 6. Apply Migrations

Once PostgreSQL credentials are fixed:

```powershell
cd backend
python manage.py migrate
```

If tenancy bootstrapping is needed afterward, create your initial tenant/domain/admin user according to your local bootstrap plan.

## 7. Run The Backend

```powershell
cd backend
python manage.py runserver
```

Backend base URL:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health/
```

## 8. Run The Frontend

```powershell
cd frontend
cmd /c npm run dev
```

Frontend base URL:

```text
http://localhost:5173
```

## 9. Quick Verification Commands

These do not require a live database to confirm code/build shape:

```powershell
python -m compileall backend
```

```powershell
cd frontend
cmd /c npm run build
```

Once PostgreSQL works, also run:

```powershell
cd backend
python manage.py check
python manage.py test
```

## 10. AI Copilot Endpoints

The backend now exposes:

- `GET /api/v1/ai/conversations/`
- `POST /api/v1/ai/conversations/`
- `POST /api/v1/ai/conversations/{conversation_id}/reply/`
- `GET /api/v1/ai/messages/?conversation={conversation_id}`

These endpoints are behind the API authentication layer already configured in Django REST Framework.

## 11. AI Copilot Test Flow

After login/auth is working and the database is migrated:

1. Create a conversation:

```http
POST /api/v1/ai/conversations/
Content-Type: application/json

{
  "tenant": "<tenant_uuid>",
  "title": "Inbound exception handling"
}
```

2. Send a prompt:

```http
POST /api/v1/ai/conversations/<conversation_uuid>/reply/
Content-Type: application/json

{
  "user_message": "A picker found damaged cartons during outbound staging. What should the floor lead do next?"
}
```

3. Inspect stored conversation messages:

```http
GET /api/v1/ai/messages/?conversation=<conversation_uuid>
```

Behavior:

- the user message is stored
- the assistant message is stored
- the OpenAI response id is persisted on the conversation for multi-turn continuity

## 12. Recommended Manual Test Pass

After backend and frontend are running:

1. Open the dashboard.
2. Open handheld receive, pick, and count screens.
3. Confirm selectors load and validation appears when fields are missing.
4. Submit operational actions and confirm success/error feedback.
5. Test the AI copilot API with a real conversation and a real `OPENAI_API_KEY`.

## 13. Current Known Blockers

- PostgreSQL auth was previously failing for `nexoflow@localhost:5432`
- live end-to-end testing depends on that being fixed
- frontend auth/session flow is still not fully wired

## 14. Push / Repo Note

This folder was not originally initialized as a git repository during the build process.

After reviewing the current files, initialize git, add the GitHub remote, commit, and push:

```powershell
git init
git branch -M main
git remote add origin git@github.com:ateba-c/NexoviaWmsG.git
git add .
git commit -m "Initial NexoFlow WMS scaffold and AI copilot wiring"
git push -u origin main
```
