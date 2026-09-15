# Cybersecurity Agent

A full-stack defensive security assistant for authorized system reviews, threat modeling, vulnerability analysis, secure implementation, and incident-response planning.

## Structure

- `frontend/`: Vite React client
- `backend/app/`: FastAPI routes, security task classifier, LLM adapter, and SQLite persistence
- `backend/tests/`: API, classifier, and configuration tests
- `docker-compose.yml`: local container orchestration

## Requirements

- Python 3.12+
- Node.js 20+
- npm 10+
- Docker Desktop (optional)

## Installation

```powershell
cd cybersecurity-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd frontend
npm install
```

Copy `.env.example` to `.env` and configure the approved LLM provider. The default local provider is Ollama and does not require an API key:

```powershell
Copy-Item .env.example .env
ollama pull llama3.2
```

Never place credentials in frontend code, `VITE_*` variables, prompts, logs, or source control. Production requires `LLM_API_KEY`, HTTPS for remote providers, and an explicit `LLM_ALLOWED_HOSTS` entry.

## Development

Terminal 1:

```powershell
cd backend
..\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8001
```

Terminal 2:

```powershell
cd frontend
npm run dev -- --port 5174
```

Open <http://localhost:5174>. The API health endpoint is <http://localhost:8001/api/health>.

## Testing

```powershell
cd backend
..\.venv\Scripts\Activate.ps1
pytest
cd ..\frontend
npm test
npm run build
```

## API

- `GET /api/health`: service health
- `GET /api/conversations`: recent security-assessment summaries
- `POST /api/chat`: send `{ "message": "...", "conversation_id": 1 }`

## Defensive-security boundaries

The agent assumes explicit authorization, uses safe testing methods, avoids requesting or exposing secrets, and does not claim vulnerabilities without evidence. Review model output against system evidence before changing a real environment. Add authentication and per-user conversation ownership before exposing this service to multiple users.

## Docker

```powershell
Copy-Item .env.example .env
docker compose up --build
```

The development UI is available at <http://localhost:5174>, and the API is available at <http://localhost:8001>.
