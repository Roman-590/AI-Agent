from __future__ import annotations

from app.core.config import settings


class TextToSpeechService:
    def __init__(self) -> None:
        self.provider = settings.tts_provider

    async def synthesize(self, text: str) -> bytes:
        if not text:
            return b""
        return text.encode("utf-8")
