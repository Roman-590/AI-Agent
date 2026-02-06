from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.services.scoring import EvaluationEngine


@dataclass
class InterviewState:
    tenant_id: str
    interview_id: str
    job_role: str = ""
    questions: list[dict[str, Any]] = field(default_factory=list)
    current_index: int = 0
    evaluations: list[dict[str, Any]] = field(default_factory=list)
    transcript: list[str] = field(default_factory=list)


class InterviewEngine:
    def __init__(self, tenant_id: str, interview_id: str) -> None:
        self.state = InterviewState(tenant_id=tenant_id, interview_id=interview_id)
        self.evaluator = EvaluationEngine()
        self.plan: dict[str, Any] = {}

    @property
    def is_complete(self) -> bool:
        return self.state.current_index >= len(self.state.questions)

    async def initialize_interview_plan(self) -> None:
        self.state.job_role = "Software Engineer"
        self.state.questions = [
            {
                "id": "intro",
                "text": "Tell me about a recent project you are proud of.",
                "category": "behavioral",
            },
            {
                "id": "technical_api",
                "text": "How would you design a low-latency WebSocket audio service?",
                "category": "technical",
            },
            {
                "id": "system_design",
                "text": "Describe how you would monitor a real-time voice interview system.",
                "category": "technical",
            },
        ]
        self.plan = {
            "job_role": self.state.job_role,
            "question_count": len(self.state.questions),
            "generated_at": datetime.utcnow().isoformat(),
        }

    async def next_question(self) -> dict[str, Any]:
        if self.is_complete:
            return {"text": "Thank you. The interview is complete."}
        question = self.state.questions[self.state.current_index]
        self.state.current_index += 1
        return {
            "id": question["id"],
            "text": question["text"],
            "category": question["category"],
            "progress": f"{self.state.current_index}/{len(self.state.questions)}",
        }

    async def evaluate_answer(self, response_text: str) -> dict[str, Any]:
        self.state.transcript.append(response_text)
        evaluation = self.evaluator.evaluate(response_text)
        self.state.evaluations.append(evaluation)
        return evaluation
