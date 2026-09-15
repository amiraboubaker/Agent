# Mobile Application Development Agent

A full-stack assistant for designing, developing, debugging, testing, optimizing, and releasing mobile applications. It covers React Native, Expo, Flutter, native Android/iOS concerns, navigation, state, APIs, authentication, maps, location, notifications, storage, performance, testing, and release preparation.

## Requirements

- Python 3.12+
- Node.js 20+
- npm 10+
- Docker Desktop (optional)

## Install

```powershell
cd mobile-application-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd frontend
npm install
```

## Run

Terminal 1:

```powershell
cd backend
..\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8004
```

Terminal 2:

```powershell
cd frontend
npm run dev
```

Open http://localhost:5174.

The default local mode works without an API key and returns a structured planning response. To use an OpenAI-compatible provider, copy `.env.example` to `.env` and configure the backend values.

## Test and build

```powershell
cd backend
..\.venv\Scripts\Activate.ps1
pytest
cd ..\frontend
npm test
npm run build
```

## API

- `GET /api/health`
- `GET /api/conversations`
- `POST /api/chat` with `{ "message": "...", "conversation_id": 1 }`

## Docker

```powershell
docker compose up --build
```

The UI is available at http://localhost:5174 and the API at http://localhost:8004.
