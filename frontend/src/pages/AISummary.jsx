import React from 'react'
import axios from 'axios'

export default function AISummary({ token, patient, onBack }) {
  const [summary, setSummary] = React.useState(null)
  const [loading, setLoading] = React.useState(true)

  React.useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/v1/patients/${patient.patient_id}/ai-summary`,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        setSummary(response.data)
      } finally {
        setLoading(false)
      }
    }
    fetchSummary()
  }, [patient, token])

  if (loading) return <div className="loading">Generating AI summary...</div>
  if (!summary) return <div>No summary available</div>

  return (
    <div className="ai-summary-container">
      <button onClick={onBack} className="btn-back">← Back</button>

      <h2>AI-Generated Clinical Summary</h2>
      <p className="patient-info">For: {patient.name} ({patient.patient_id})</p>

      <div className="disclaimer">
        <strong>⚠️ DISCLAIMER:</strong>
        {summary.disclaimer}
      </div>

      {summary.conditions && (
        <div className="summary-section">
          <h3>📋 Conditions (Confidence: {summary.conditions.confidence})</h3>
          {summary.conditions.items.map((condition, idx) => (
            <div key={idx} className="summary-item">
              <strong>{condition.name}</strong>
              <p>Status: {condition.status}</p>
              <p className="data-meta">Since: {condition.since}</p>
              {condition.sources.map((source, sidx) => (
                <div key={sidx} className="source">
                  📄 {source.document_name} ({source.date})
                </div>
              ))}
            </div>
          ))}
        </div>
      )}

      {summary.medications && (
        <div className="summary-section">
          <h3>💊 Medications (Confidence: {summary.medications.confidence})</h3>
          {summary.medications.items.map((med, idx) => (
            <div key={idx} className="summary-item">
              <strong>{med.name}</strong>
              <p>{med.dose} - {med.frequency}</p>
              <p className="data-meta">Since: {med.since}</p>
            </div>
          ))}
        </div>
      )}

      {summary.allergies && (
        <div className="summary-section critical">
          <h3>⚠️ Allergies (Confidence: {summary.allergies.confidence})</h3>
          {summary.allergies.items.map((allergy, idx) => (
            <div key={idx} className="summary-item">
              <strong>{allergy.substance}</strong>
              <p>Reaction: {allergy.reaction}</p>
              <p className={`severity-${allergy.severity.toLowerCase()}`}>
                {allergy.severity}
              </p>
            </div>
          ))}
        </div>
      )}

      {summary.clinical_notes && (
        <div className="summary-section">
          <h3>📝 Clinical Notes</h3>
          <p>{summary.clinical_notes}</p>
        </div>
      )}

      <div className="summary-footer">
        Generated: {new Date(summary.generated_at).toLocaleString()}
      </div>
    </div>
  )
}
