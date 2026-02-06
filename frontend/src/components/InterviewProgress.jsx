export default function InterviewProgress({ evaluation, status }) {
  return (
    <section className="progress-panel">
      <h2>Interview Progress</h2>
      <p>Status: {status}</p>
      {evaluation ? (
        <ul>
          <li>Communication: {evaluation.communication}</li>
          <li>Technical: {evaluation.technical}</li>
          <li>Confidence: {evaluation.confidence}</li>
          <li>Sentiment: {evaluation.sentiment}</li>
        </ul>
      ) : (
        <p>No evaluation yet.</p>
      )}
    </section>
  );
}
