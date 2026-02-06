import { useEffect, useMemo, useState } from "react";

import InterviewProgress from "../components/InterviewProgress";
import TranscriptPanel from "../components/TranscriptPanel";
import useVoiceWebSocket from "../hooks/useVoiceWebSocket";

const tenantId = "demo-tenant";
const interviewId = "demo-interview";

export default function VoiceInterviewPage() {
  const [transcript, setTranscript] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [evaluation, setEvaluation] = useState(null);
  const [status, setStatus] = useState("idle");

  const wsUrl = useMemo(
    () => `ws://localhost:8000/api/voice/stream/${tenantId}/${interviewId}`,
    []
  );

  const { sendEvent, lastEvent } = useVoiceWebSocket(wsUrl);

  useEffect(() => {
    if (!lastEvent) {
      return;
    }
    if (lastEvent.event === "interview_started") {
      setStatus("active");
      sendEvent({ event: "candidate_ready" });
    }
    if (lastEvent.event === "question") {
      setCurrentQuestion(lastEvent);
    }
    if (lastEvent.event === "evaluation") {
      setEvaluation(lastEvent);
      setTranscript((prev) => [...prev, { text: lastEvent.response || "" }]);
    }
    if (lastEvent.event === "interview_complete") {
      setStatus("complete");
    }
  }, [lastEvent, sendEvent]);

  const handleStart = () => {
    setStatus("connecting");
    sendEvent({ event: "candidate_ready" });
  };

  return (
    <div className="voice-interview">
      <header>
        <h1>Voice AI Interviewer</h1>
        <p>Status: {status}</p>
      </header>

      <section className="question-panel">
        <h2>Current Question</h2>
        <p>{currentQuestion?.text || "Waiting for question..."}</p>
      </section>

      <InterviewProgress evaluation={evaluation} status={status} />

      <TranscriptPanel transcript={transcript} />

      <button type="button" onClick={handleStart}>
        Start Interview
      </button>
    </div>
  );
}
