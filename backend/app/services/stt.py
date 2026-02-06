from __future__ import annotations

from app.core.config import settings


class SpeechToTextService:
    def __init__(self) -> None:
        self.provider = settings.stt_provider

    async def transcribe(self, audio_bytes: bytes) -> str:
        if not audio_bytes:
            return ""
        return f"[transcript:{len(audio_bytes)} bytes via {self.provider}]"
