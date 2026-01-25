interface AISummaryCardProps {
  summary: any
}

export default function AISummaryCard({ summary }: AISummaryCardProps) {
  return (
    <div className="ai-summary-card">
      <div className="summary-section">
        <h2>Summary</h2>
        <p>{summary.clinical_notes}</p>
      </div>

      {summary.conditions && (
        <div className="summary-section">
          <h3>Conditions</h3>
          {summary.conditions.items?.map((item: any) => (
            <div key={item.name} className="summary-item">
              <strong>{item.name}</strong>
              <p>Status: {item.status}</p>
              {item.sources?.length > 0 && (
                <p className="source-info">Sources: {item.sources.map((s: any) => s.document_name).join(', ')}</p>
              )}
            </div>
          ))}
        </div>
      )}

      {summary.medications && (
        <div className="summary-section">
          <h3>Medications</h3>
          {summary.medications.items?.map((item: any) => (
            <div key={item.name} className="summary-item">
              <strong>{item.name}</strong>
              <p>{item.dose} {item.frequency}</p>
            </div>
          ))}
        </div>
      )}

      {summary.allergies && (
        <div className="summary-section critical">
          <h3>⚠️ Allergies</h3>
          {summary.allergies.items?.map((item: any) => (
            <div key={item.substance} className="summary-item">
              <strong>{item.substance}</strong>
              <p>Reaction: {item.reaction}</p>
              <p>Severity: {item.severity}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
