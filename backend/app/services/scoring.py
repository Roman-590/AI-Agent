from __future__ import annotations

from statistics import mean


class EvaluationEngine:
    def __init__(self) -> None:
        self.rubric = {
            "communication": 0.0,
            "technical": 0.0,
            "confidence": 0.0,
        }

    def evaluate(self, response_text: str) -> dict[str, float]:
        length_score = min(len(response_text) / 200, 1.0)
        confidence_score = 0.5 + length_score / 2
        technical_score = 0.6 + length_score / 3
        communication_score = 0.5 + length_score / 4
        return {
            "communication": round(communication_score, 2),
            "technical": round(technical_score, 2),
            "confidence": round(confidence_score, 2),
            "sentiment": round(mean([confidence_score, communication_score]), 2),
        }
