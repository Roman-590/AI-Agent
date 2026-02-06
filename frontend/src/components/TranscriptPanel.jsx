export default function TranscriptPanel({ transcript }) {
  return (
    <section className="transcript-panel">
      <h2>Live Transcript</h2>
      <div className="transcript">
        {transcript.length === 0 ? (
          <p>No transcript yet.</p>
        ) : (
          transcript.map((entry, index) => (
            <p key={index}>{entry.text || "..."}</p>
          ))
        )}
      </div>
    </section>
  );
}
