from __future__ import annotations

import json
from pathlib import Path

from app.core.config import settings


class InterviewStorage:
    def __init__(self, tenant_id: str) -> None:
        self.tenant_id = tenant_id
        self.audio_path = Path(settings.audio_storage_path) / tenant_id
        self.transcript_path = Path(settings.transcripts_path) / tenant_id
        self.audio_path.mkdir(parents=True, exist_ok=True)
        self.transcript_path.mkdir(parents=True, exist_ok=True)

    async def append_transcript(self, interview_id: str, transcript: str) -> None:
        file_path = self.transcript_path / f"{interview_id}.log"
        with file_path.open("a", encoding="utf-8") as handle:
            handle.write(transcript + "\n")

    async def save_report(self, report: dict[str, object]) -> None:
        file_path = self.transcript_path / f"{report['interview_id']}.json"
        with file_path.open("w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)

    async def save_partial(self, engine: object) -> None:
        file_path = self.transcript_path / f"{getattr(engine.state, 'interview_id', 'unknown')}.partial"
        with file_path.open("w", encoding="utf-8") as handle:
            handle.write("connection dropped")

    async def fetch_report(self, interview_id: str) -> dict[str, object]:
        file_path = self.transcript_path / f"{interview_id}.json"
        if not file_path.exists():
            return {"error": "report not found"}
        with file_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
