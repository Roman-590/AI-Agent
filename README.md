# Voice AI Interviewer Module

Production-ready starter kit for a real-time Voice AI Interviewer integrated into a SaaS recruiting platform.

## Features
- FastAPI voice service with WebSocket streaming
- Whisper/OpenAI STT + OpenAI/ElevenLabs TTS pluggable services
- LangGraph-ready interview engine with adaptive evaluations
- React voice interview UI with live transcript + progress tracker
- Structured interview reports (JSON + summary)
- Tenant-aware storage paths and usage metering schema

## Project Structure
```
backend/
  app/
    api/voice.py
    core/config.py
    services/
frontend/
  src/
    pages/VoiceInterviewPage.jsx
    components/
    hooks/
```

## Setup

### Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker compose up --build
```

## Example Interview Script
See [docs/voice_interview_script.md](docs/voice_interview_script.md).

## API Highlights
- `ws://localhost:8000/api/voice/stream/{tenant_id}/{interview_id}`
- `GET /api/voice/report/{tenant_id}/{interview_id}`

## Report Output (JSON)
```json
{
  "interview_id": "demo-interview",
  "job_role": "Software Engineer",
  "transcript": ["..."],
  "evaluations": [{"communication": 0.7, "technical": 0.8, "confidence": 0.75}],
  "scores": {"communication": 0.7, "technical": 0.8, "confidence": 0.75},
  "recommendation": "Maybe",
  "summary": "Overall communication score: 0.7. Technical depth: 0.8. Confidence: 0.75. Recommendation: Maybe."
}
```

## Next Steps
- Wire Whisper/OpenAI STT + ElevenLabs TTS providers
- Persist interviews into your existing SaaS database layer
- Attach recordings to the recruiter dashboard for replay
- Add monitoring hooks and metrics collection
