import { useState, useEffect } from 'react'

const API_BASE = 'http://localhost:8000'

function AISummary({ token, patient, onBack }) {
  const [summaryData, setSummaryData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadAISummary = async () => {
      try {
        const response = await fetch(
          `${API_BASE}/api/v1/patients/${patient.patient_id}/ai-summary`,
          {
            headers: { 'Authorization': `Bearer ${token}` }
          }
        )

        if (!response.ok) {
          throw new Error('Failed to load AI summary')
        }

        const data = await response.json()
        setSummaryData(data)
      } catch (err) {
        console.error('Error loading AI summary:', err)
      } finally {
        setLoading(false)
      }
    }

    loadAISummary()
  }, [token, patient.patient_id])

  if (loading) {
    return (
      <div className="page-container">
        <p>Loading AI summary...</p>
      </div>
    )
  }

  if (!summaryData) {
    return (
      <div className="page-container">
        <p>Error loading AI summary</p>
      </div>
    )
  }

  return (
    <div className="page-container">
      <header className="page-header">
        <div className="header-content">
          <div className="header-left">
            <button onClick={onBack} className="btn-secondary">← Back to Patient</button>
            <h1>AI-Generated Summary</h1>
          </div>
        </div>
      </header>

      <div className="content">
        <div className="ai-summary-container">
          <div className="ai-disclaimer">
            <p>{summaryData.disclaimer}</p>
            <p><strong>Patient:</strong> {summaryData.patient_name}</p>
            <p><strong>Generated:</strong> {new Date(summaryData.generated_at).toLocaleString()}</p>
          </div>

          <div className="ai-section">
            <h2>CONDITIONS</h2>
            {summaryData.summary.conditions.map((condition, idx) => (
              <div key={idx} className="ai-item">
                <h3>{condition.name}</h3>
                <p><strong>Status:</strong> {condition.status}</p>
                <p><strong>Diagnosed:</strong> {condition.diagnosed_date}</p>
                <p><strong>ICD Code:</strong> {condition.icd_code}</p>
                <p className="ai-confidence">Confidence: {condition.confidence}</p>
                <p className="ai-source">Source: {condition.source}</p>
              </div>
            ))}
          </div>

          <div className="ai-section">
            <h2>MEDICATIONS</h2>
            {summaryData.summary.medications.map((med, idx) => (
              <div key={idx} className="ai-item">
                <h3>{med.name} ({med.dose})</h3>
                <p><strong>Frequency:</strong> {med.frequency}</p>
                <p><strong>Indication:</strong> {med.indication}</p>
                <p><strong>Prescriber:</strong> {med.prescriber}</p>
                <p className="ai-confidence">Confidence: {med.confidence}</p>
                <p className="ai-source">Source: {med.source}</p>
              </div>
            ))}
          </div>

          <div className="ai-section allergies-critical">
            <h2>ALLERGIES (CRITICAL)</h2>
            {summaryData.summary.allergies.map((allergy, idx) => (
              <div key={idx} className={`ai-item allergy-${allergy.severity.toLowerCase()}`}>
                <h3>{allergy.substance}</h3>
                <p><strong>Severity:</strong> {allergy.severity}</p>
                <p><strong>Reaction:</strong> {allergy.reaction}</p>
                <p className="ai-confidence">Confidence: {allergy.confidence}</p>
                <p className="ai-source">Source: {allergy.source}</p>
              </div>
            ))}
          </div>

          <div className="ai-section">
            <h2>RECENT TESTS</h2>
            {summaryData.summary.recent_tests.map((test, idx) => (
              <div key={idx} className={`ai-item test-${test.status.toLowerCase()}`}>
                <h3>{test.test}</h3>
                <p><strong>Value:</strong> {test.value}</p>
                <p><strong>Date:</strong> {test.date}</p>
                <p><strong>Status:</strong> {test.status}</p>
                <p className="ai-confidence">Confidence: {test.confidence}</p>
                <p className="ai-source">Source: {test.source}</p>
              </div>
            ))}
          </div>

          {summaryData.summary.implants_devices.length > 0 && (
            <div className="ai-section">
              <h2>IMPLANTS/DEVICES</h2>
              {summaryData.summary.implants_devices.map((device, idx) => (
                <div key={idx} className="ai-item">
                  <h3>{device.type}</h3>
                  <p><strong>Model:</strong> {device.model}</p>
                  <p><strong>Implanted:</strong> {device.date_implanted}</p>
                  <p className="ai-confidence">Confidence: {device.confidence}</p>
                  <p className="ai-source">Source: {device.source}</p>
                </div>
              ))}
            </div>
          )}

          <div className="ai-limitations">
            <h3>AI Limitations</h3>
            <ul>
              {summaryData.ai_limitations.map((limitation, idx) => (
                <li key={idx}>{limitation}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AISummary
