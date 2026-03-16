# Jarvis AI Assistant

Production-level Jarvis-style **browser voice assistant** with:
- **Instant automation** (no LLM delay for system actions)
- **Context-aware conversation** (session memory)
- **Multilingual pipeline** (English/Hindi/Telugu detect; optional translation service)
- **Security hooks** (voice phrase + PIN login endpoints)

## Backend (FastAPI)

Create env file:

```bash
cd backend
cp .env.example .env
```

Install + run:

```bash
cd backend
python3 -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend (React)

```bash
cd frontend
npm install
npm start
```

## Ollama (local LLM)

Install Ollama, then:

```bash
ollama run mistral
```

## Demo commands (instant lane)

- **Open Chrome**: `open chrome`
- **Open Pictures**: `open pictures`
- **Open Downloads**: `open downloads`
- **File search**: `find <filename>`

## Notes

- **Translation**: set `JARVIS_TRANSLATE_PROVIDER=libretranslate` and run a LibreTranslate endpoint, or keep `noop` (default) to avoid external dependencies.
- **Security**: configure `JARVIS_VOICE_PASSPHRASE_HASH` and `JARVIS_PIN_HASH` in `backend/.env` (bcrypt hashes). Auth endpoints:
  - `POST /auth/voice` with `{ "phrase": "..." }`
  - `POST /auth/pin` with `{ "pin": "..." }`