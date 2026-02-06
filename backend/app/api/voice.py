from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.audio import AudioStreamManager
from app.services.interview import InterviewEngine
from app.services.reporting import InterviewReportBuilder
from app.services.storage import InterviewStorage

router = APIRouter()


@router.websocket("/stream/{tenant_id}/{interview_id}")
async def stream_interview_audio(
    websocket: WebSocket, tenant_id: str, interview_id: str
) -> None:
    await websocket.accept()
    audio_manager = AudioStreamManager(tenant_id=tenant_id, interview_id=interview_id)
    interview_engine = InterviewEngine(tenant_id=tenant_id, interview_id=interview_id)
    report_builder = InterviewReportBuilder()
    storage = InterviewStorage(tenant_id=tenant_id)

    await interview_engine.initialize_interview_plan()

    try:
        await websocket.send_json(
            {
                "event": "interview_started",
                "timestamp": datetime.utcnow().isoformat(),
                "plan": interview_engine.plan,
            }
        )

        while True:
            payload = await websocket.receive()
            if payload.get("type") == "websocket.disconnect":
                raise WebSocketDisconnect

            if "bytes" in payload:
                await audio_manager.enqueue_audio(payload["bytes"])

            if "text" in payload:
                message = json.loads(payload["text"])
                event_type = message.get("event")

                if event_type == "candidate_ready":
                    next_question = await interview_engine.next_question()
                    await websocket.send_json({"event": "question", **next_question})
                    continue

                if event_type == "candidate_response":
                    response_text = message.get("text", "")
                    evaluation = await interview_engine.evaluate_answer(response_text)
                    await websocket.send_json({"event": "evaluation", **evaluation})

                    if interview_engine.is_complete:
                        report = report_builder.build(interview_engine)
                        await storage.save_report(report)
                        await websocket.send_json(
                            {
                                "event": "interview_complete",
                                "report": report,
                            }
                        )
                        break

                    follow_up = await interview_engine.next_question()
                    await websocket.send_json({"event": "question", **follow_up})

            await audio_manager.flush_ready_audio()

    except WebSocketDisconnect:
        await storage.save_partial(interview_engine)
    finally:
        await audio_manager.close()


@router.get("/report/{tenant_id}/{interview_id}")
async def get_report(tenant_id: str, interview_id: str) -> dict[str, Any]:
    storage = InterviewStorage(tenant_id=tenant_id)
    return await storage.fetch_report(interview_id)
