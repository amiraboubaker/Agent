# Product Management Agent

Product Management Agent turns ideas and problems into practical, validated, executable product plans. It identifies target users, keeps the MVP small, prioritizes business and user value, separates validated facts from hypotheses, and recommends experiments for risky assumptions.

Product plans are displayed as Markdown with syntax highlighting and can be copied. The application does not present unvalidated assumptions as facts and keeps API keys on the backend.

## Structure

- `frontend/`: Vite React client
- `backend/app/`: FastAPI routes, task classifier, LLM adapter, SQLite persistence
- `backend/tests/`: API and classifier tests
- `docker-compose.yml`: local container orchestration

## Requirements

- Python 3.12+
- Node.js 20+
- npm 10+
- Docker Desktop (optional)

## Installation

```powershell
cd product-management-agent
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd frontend
npm install
```

On macOS/Linux, activate the environment with `source .venv/bin/activate`.

## Environment configuration

Edit `.env`:

```env
LLM_API_URL=http://localhost:11434/v1/chat/completions
LLM_API_KEY=
LLM_MODEL=llama3.2
DATABASE_URL=sqlite:///./data/agent.db
CORS_ORIGINS=http://localhost:5173
LLM_ALLOWED_HOSTS=localhost,127.0.0.1,api.openai.com
RATE_LIMIT_PER_MINUTE=20
```

The default local provider is Ollama, which runs on your computer and does not require an API key or credits. Install Ollama from <https://ollama.com>, then download the configured model:

```powershell
ollama pull llama3.2
```

Start Ollama before starting the backend. Restart the backend after changing `.env` because settings are loaded at startup. Never put a cloud provider key in frontend code or a `VITE_*` variable.

For Docker Desktop on Windows, Compose automatically changes the Ollama host to `host.docker.internal`, which lets the container reach Ollama running on the host.

To use a remote OpenAI-compatible provider instead, set its HTTPS URL, model, and key in your local environment. For GitHub Actions, add a repository secret named `LLM_API_KEY` under **Settings > Secrets and variables > Actions** and pass it to the backend process:

```yaml
env:
  LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
```

When using Docker Compose in that workflow, the backend receives the value through its environment. Do not write the secret to a file, include it in a Docker image, or print it in workflow logs. GitHub Secrets are available only inside Actions; a separately hosted production server must configure the same variable in its own secret manager.

Set `APP_ENV=production` for a remote production provider. Production startup fails if `LLM_API_KEY` is missing. `LLM_ALLOWED_HOSTS` limits outbound AI requests to approved hosts, permits local Ollama over HTTP, and requires HTTPS for remote hosts. `RATE_LIMIT_PER_MINUTE` limits chat requests per client IP.

## Development

Terminal 1:

```powershell
cd backend
..\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

Terminal 2:

```powershell
cd frontend
npm run dev
```

Open <http://localhost:5173>.

## Testing

Backend:

```powershell
cd backend
..\.venv\Scripts\Activate.ps1
pytest
```

Frontend:

```powershell
cd frontend
npm test
npm run build
```

## API

- `GET /api/health`: service health
- `GET /api/conversations`: recent conversation summaries
- `POST /api/chat`: send `{ "message": "...", "conversation_id": 1 }`

## Docker

```powershell
Copy-Item .env.example .env
docker compose up --build
```

The development UI is available at <http://localhost:5173>, and the API is available at <http://localhost:8000>.

## Production build

Build the frontend:

```powershell
cd frontend
npm run build
```

For production, serve `frontend/dist` from a static host or Nginx and run the FastAPI service behind a production ASGI process such as Gunicorn with Uvicorn workers. Set a specific production `CORS_ORIGINS`, use a managed database when needed, and inject `LLM_API_KEY` through the deployment secret manager.

## Security notes

- API keys are read only by the backend.
- Pydantic validates and bounds request input.
- CORS is explicitly configured through environment variables; use only the exact production frontend origin.
- The backend applies basic per-IP chat rate limiting and security response headers.
- Production requires an LLM key and only permits configured HTTPS LLM hosts.
- Add user authentication and per-user conversation ownership before exposing this service to multiple users.
- Generated code is never executed by the service.
- Review model output before using it in a real project.
