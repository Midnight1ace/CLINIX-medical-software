import { useState, useEffect } from 'react'

const API_BASE = 'http://localhost:8000'

function AISummary({ token, patient, onBack }) {
  const [summaryData, setSummaryData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [advancedMode, setAdvancedMode] = useState(false)

  useEffect(() => {
    const loadAISummary = async () => {
      try {
        const response = await fetch(
          `${API_BASE}/api/v1/patients/${patient.patient_id}/ai-summary${advancedMode ? '?mode=advanced' : ''}`,
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
  }, [token, patient.patient_id, advancedMode])

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
            <h1>AI-Generated Clinical Summary</h1>
          </div>
          <div className="header-right">
            <button
              onClick={() => setAdvancedMode(!advancedMode)}
              className="btn-secondary"
            >
              {advancedMode ? 'Advanced: On' : 'Advanced: Off'}
            </button>
          </div>
        </div>
      </header>

      <div className="content">
        <div className="ai-summary-container">
          <div className="ai-disclaimer">
            <p style={{ fontSize: '14px', color: '#e67e22', fontWeight: 'bold' }}>
              {summaryData.disclaimer}
            </p>
            <div style={{ display: 'flex', gap: '20px', marginTop: '10px', fontSize: '13px' }}>
              <span><strong>Patient:</strong> {summaryData.patient_name}</span>
              <span><strong>Generated:</strong> {new Date(summaryData.generated_at).toLocaleString()}</span>
              {summaryData.ai_model && (
                <span><strong>AI Model:</strong> {summaryData.ai_model}</span>
              )}
            </div>
          </div>

          {/* Gemini AI Generated Summary */}
          {summaryData.ai_generated_summary && (
            <div style={{
              backgroundColor: '#f0f8ff',
              border: '2px solid #3498db',
              borderRadius: '8px',
              padding: '20px',
              marginBottom: '20px'
            }}>
              <h2 style={{ 
                fontSize: '18px', 
                fontWeight: 'bold', 
                marginBottom: '15px',
                color: '#2c3e50',
                borderBottom: '2px solid #3498db',
                paddingBottom: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '10px'
              }}>
                🤖 AI-Generated Clinical Summary
              </h2>
              <div style={{
                fontSize: '14px',
                lineHeight: '1.8',
                color: '#34495e',
                whiteSpace: 'pre-wrap'
              }}>
                {summaryData.ai_generated_summary}
              </div>
            </div>
          )}

          {summaryData.advanced && (
            <div style={{
              backgroundColor: '#fff9e6',
              border: '2px solid #f1c40f',
              borderRadius: '8px',
              padding: '20px',
              marginBottom: '20px'
            }}>
              <h2 style={{
                fontSize: '18px',
                fontWeight: 'bold',
                marginBottom: '15px',
                color: '#8e6f00',
                borderBottom: '2px solid #f1c40f',
                paddingBottom: '8px'
              }}>
                Advanced AI Insights
              </h2>
              {summaryData.advanced.interaction_analysis && (
                <div style={{ marginBottom: '15px', fontSize: '14px' }}>
                  <strong>Medication Interactions</strong>
                  <pre style={{ whiteSpace: 'pre-wrap', marginTop: '8px' }}>
                    {JSON.stringify(summaryData.advanced.interaction_analysis, null, 2)}
                  </pre>
                </div>
              )}
              {summaryData.advanced.emergency_insights && (
                <div style={{ fontSize: '14px' }}>
                  <strong>Emergency Insights</strong>
                  <div style={{ whiteSpace: 'pre-wrap', marginTop: '8px' }}>
                    {summaryData.advanced.emergency_insights}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Clinical Overview Box */}
          <div className="summary-box" style={{
            backgroundColor: '#f8f9fa',
            border: '2px solid #dee2e6',
            borderRadius: '8px',
            padding: '20px',
            marginBottom: '20px'
          }}>
            <h2 style={{ 
              fontSize: '18px', 
              fontWeight: 'bold', 
              marginBottom: '15px',
              color: '#2c3e50',
              borderBottom: '2px solid #3498db',
              paddingBottom: '8px'
            }}>
              CLINICAL OVERVIEW
            </h2>
            
            {/* Vital Signs */}
            {summaryData.summary.recent_visits && summaryData.summary.recent_visits.length > 0 && (
              <div style={{ marginBottom: '15px' }}>
                <h3 style={{ fontSize: '15px', fontWeight: '600', color: '#34495e', marginBottom: '8px' }}>
                  Latest Visit
                </h3>
                {summaryData.summary.recent_visits.slice(0, 1).map((visit, idx) => (
                  <div key={idx} style={{ 
                    backgroundColor: 'white', 
                    padding: '12px', 
                    borderRadius: '6px',
                    border: '1px solid #e0e0e0'
                  }}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '13px' }}>
                      <div><strong>Date:</strong> {visit.date}</div>
                      <div><strong>Type:</strong> {visit.type}</div>
                      <div><strong>Provider:</strong> {visit.provider}</div>
                      <div><strong>Facility:</strong> {visit.facility}</div>
                      <div style={{ gridColumn: '1 / -1' }}><strong>Chief Complaint:</strong> {visit.chief_complaint}</div>
                      <div style={{ gridColumn: '1 / -1' }}><strong>Diagnosis:</strong> {visit.diagnosis}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Diagnoses */}
            {summaryData.summary.recent_diagnoses && summaryData.summary.recent_diagnoses.length > 0 && (
              <div style={{ marginBottom: '15px' }}>
                <h3 style={{ fontSize: '15px', fontWeight: '600', color: '#34495e', marginBottom: '8px' }}>
                  Recent Diagnoses
                </h3>
                <div style={{ backgroundColor: 'white', padding: '12px', borderRadius: '6px', border: '1px solid #e0e0e0' }}>
                  {summaryData.summary.recent_diagnoses.map((diag, idx) => (
                    <div key={idx} style={{ 
                      marginBottom: idx < summaryData.summary.recent_diagnoses.length - 1 ? '8px' : '0',
                      paddingBottom: idx < summaryData.summary.recent_diagnoses.length - 1 ? '8px' : '0',
                      borderBottom: idx < summaryData.summary.recent_diagnoses.length - 1 ? '1px solid #f0f0f0' : 'none'
                    }}>
                      <div style={{ fontSize: '13px' }}>
                        <strong>{diag.diagnosis}</strong>
                        <span style={{ marginLeft: '10px', color: '#7f8c8d' }}>({diag.date})</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Conditions */}
            {summaryData.summary.conditions && summaryData.summary.conditions.length > 0 && (
              <div style={{ marginBottom: '15px' }}>
                <h3 style={{ fontSize: '15px', fontWeight: '600', color: '#34495e', marginBottom: '8px' }}>
                  Chronic Conditions
                </h3>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {summaryData.summary.conditions.map((condition, idx) => (
                    <span key={idx} style={{
                      backgroundColor: '#3498db',
                      color: 'white',
                      padding: '6px 12px',
                      borderRadius: '20px',
                      fontSize: '12px',
                      fontWeight: '500'
                    }}>
                      {condition.name}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Allergies - Highlighted */}
            {summaryData.summary.allergies && summaryData.summary.allergies.length > 0 && (
              <div style={{ marginBottom: '15px' }}>
                <h3 style={{ 
                  fontSize: '15px', 
                  fontWeight: '600', 
                  color: '#c0392b', 
                  marginBottom: '8px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px'
                }}>
                  ⚠️ Allergies
                </h3>
                <div style={{ backgroundColor: '#ffe6e6', padding: '12px', borderRadius: '6px', border: '2px solid #e74c3c' }}>
                  {summaryData.summary.allergies.map((allergy, idx) => (
                    <div key={idx} style={{ 
                      marginBottom: idx < summaryData.summary.allergies.length - 1 ? '10px' : '0',
                      paddingBottom: idx < summaryData.summary.allergies.length - 1 ? '10px' : '0',
                      borderBottom: idx < summaryData.summary.allergies.length - 1 ? '1px solid #ffcccc' : 'none'
                    }}>
                      <div style={{ fontSize: '14px', fontWeight: 'bold', color: '#c0392b' }}>
                        {allergy.substance} ({allergy.severity})
                      </div>
                      <div style={{ fontSize: '12px', color: '#555', marginTop: '4px' }}>
                        Reaction: {allergy.reaction}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Medications */}
            {summaryData.summary.medications && summaryData.summary.medications.length > 0 && (
              <div>
                <h3 style={{ fontSize: '15px', fontWeight: '600', color: '#34495e', marginBottom: '8px' }}>
                  Current Medications
                </h3>
                <div style={{ backgroundColor: 'white', padding: '12px', borderRadius: '6px', border: '1px solid #e0e0e0' }}>
                  {summaryData.summary.medications.map((med, idx) => (
                    <div key={idx} style={{ 
                      marginBottom: idx < summaryData.summary.medications.length - 1 ? '10px' : '0',
                      paddingBottom: idx < summaryData.summary.medications.length - 1 ? '10px' : '0',
                      borderBottom: idx < summaryData.summary.medications.length - 1 ? '1px solid #f0f0f0' : 'none'
                    }}>
                      <div style={{ fontSize: '13px' }}>
                        <strong style={{ color: '#2c3e50' }}>{med.name}</strong>
                        <span style={{ marginLeft: '8px', color: '#7f8c8d' }}>{med.dose}</span>
                        <span style={{ marginLeft: '8px', color: '#95a5a6' }}>• {med.frequency}</span>
                      </div>
                      {med.indication !== 'See record' && (
                        <div style={{ fontSize: '12px', color: '#7f8c8d', marginTop: '4px' }}>
                          Indication: {med.indication}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="ai-limitations" style={{
            backgroundColor: '#ecf0f1',
            padding: '15px',
            borderRadius: '6px',
            border: '1px solid #bdc3c7'
          }}>
            <h3 style={{ fontSize: '14px', fontWeight: '600', marginBottom: '8px', color: '#34495e' }}>
              AI Limitations
            </h3>
            <ul style={{ margin: '0', paddingLeft: '20px', fontSize: '12px', color: '#555' }}>
              {summaryData.ai_limitations.map((limitation, idx) => (
                <li key={idx} style={{ marginBottom: '4px' }}>{limitation}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AISummary
