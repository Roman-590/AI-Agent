from __future__ import annotations

import asyncio
from collections import deque

from app.services.stt import SpeechToTextService
from app.services.storage import InterviewStorage


class AudioStreamManager:
    def __init__(self, tenant_id: str, interview_id: str) -> None:
        self.tenant_id = tenant_id
        self.interview_id = interview_id
        self.buffer: deque[bytes] = deque()
        self.stt = SpeechToTextService()
        self.storage = InterviewStorage(tenant_id=tenant_id)
        self._closed = False

    async def enqueue_audio(self, chunk: bytes) -> None:
        self.buffer.append(chunk)

    async def flush_ready_audio(self) -> None:
        if not self.buffer:
            return
        batch = b"".join(self.buffer)
        self.buffer.clear()
        transcript = await self.stt.transcribe(batch)
        if transcript:
            await self.storage.append_transcript(
                interview_id=self.interview_id,
                transcript=transcript,
            )

    async def close(self) -> None:
        if self._closed:
            return
        await asyncio.sleep(0)
        self._closed = True
