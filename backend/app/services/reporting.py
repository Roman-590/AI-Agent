from __future__ import annotations

from statistics import mean

from app.services.interview import InterviewEngine


class InterviewReportBuilder:
    def build(self, engine: InterviewEngine) -> dict[str, object]:
        evaluations = engine.state.evaluations
        transcript = engine.state.transcript

        def avg(metric: str) -> float:
            if not evaluations:
                return 0.0
            return round(mean(item.get(metric, 0.0) for item in evaluations), 2)

        communication = avg("communication")
        technical = avg("technical")
        confidence = avg("confidence")
        recommendation = self._recommendation(communication, technical, confidence)

        summary = (
            f"Overall communication score: {communication}. "
            f"Technical depth: {technical}. Confidence: {confidence}. "
            f"Recommendation: {recommendation}."
        )

        return {
            "interview_id": engine.state.interview_id,
            "job_role": engine.state.job_role,
            "transcript": transcript,
            "evaluations": evaluations,
            "scores": {
                "communication": communication,
                "technical": technical,
                "confidence": confidence,
            },
            "recommendation": recommendation,
            "summary": summary,
        }

    def _recommendation(self, communication: float, technical: float, confidence: float) -> str:
        average = mean([communication, technical, confidence])
        if average >= 0.8:
            return "Hire"
        if average >= 0.6:
            return "Maybe"
        return "Reject"
