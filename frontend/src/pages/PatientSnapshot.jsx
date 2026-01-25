import React from 'react'
import axios from 'axios'

export default function PatientSnapshot({ token, patient, onEmergency, onHistory, onBack }) {
  const [snapshot, setSnapshot] = React.useState(null)
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState('')

  React.useEffect(() => {
    const fetchSnapshot = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/v1/patients/${patient.patient_id}/snapshot`,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        setSnapshot(response.data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    fetchSnapshot()
  }, [patient, token])

  if (loading) return <div className="loading">Loading patient snapshot...</div>
  if (error) return <div className="error-message">❌ Error: {error}</div>
  if (!snapshot) return <div className="error-message">No data available</div>

  return (
    <div className="snapshot-container">
      <button onClick={onBack} className="btn-back">← Back to Search</button>

      {/* PATIENT HEADER */}
      <div className="patient-header">
        <h2>{snapshot.patient.name}</h2>
        <p>
          ID: {snapshot.patient.patient_id} | DOB: {snapshot.patient.date_of_birth} | 
          Age: {snapshot.patient.age} | Blood Type: {snapshot.patient.blood_type}
        </p>
      </div>

      {/* ALERT BANNER */}
      {snapshot.alerts && snapshot.alerts.length > 0 && (
        <div className="alert-banner critical">
          <h3>🚨 CRITICAL ALERTS</h3>
          {snapshot.alerts.map((alert) => (
            <div key={alert.alert_id} className="alert-item">
              <strong>⚠️ {alert.message}</strong>
            </div>
          ))}
        </div>
      )}

      {/* TWO-COLUMN LAYOUT */}
      <div className="snapshot-grid">
        {/* LEFT: STABLE DATA */}
        <div className="stable-data">
          <h3>🔒 Stable Medical Data</h3>
          
          <div className="data-section">
            <h4>🩸 Blood Type</h4>
            <p className="data-value">{snapshot.stable_data.blood_type.value}</p>
            <p className="data-meta">Verified: {snapshot.stable_data.blood_type.verified_date}</p>
          </div>

          <div className="data-section">
            <h4>⚠️ Allergies</h4>
            {snapshot.stable_data.allergies.map((allergy, idx) => (
              <div key={idx} className="allergy-item">
                <strong>{allergy.substance}</strong> → {allergy.reaction}
                <br />
                <span className={`severity-${allergy.severity.toLowerCase()}`}>
                  {allergy.severity}
                </span>
              </div>
            ))}
          </div>

          <div className="data-section">
            <h4>❤️ Chronic Conditions</h4>
            {snapshot.stable_data.chronic_conditions.map((condition, idx) => (
              <div key={idx} className="condition-item">
                <strong>{condition.name}</strong>
                <br />
                <span className="data-meta">Since: {condition.diagnosis_date}</span>
              </div>
            ))}
          </div>

          {snapshot.stable_data.implants_devices && snapshot.stable_data.implants_devices.length > 0 && (
            <div className="data-section">
              <h4>🏥 Implants/Devices</h4>
              {snapshot.stable_data.implants_devices.map((device, idx) => (
                <div key={idx} className="device-item">
                  <strong>{device.type}</strong> (Implanted: {device.implant_date})
                </div>
              ))}
            </div>
          )}
        </div>

        {/* RIGHT: DYNAMIC DATA */}
        <div className="dynamic-data">
          <h3>📊 Current Clinical Status</h3>

          <div className="data-section">
            <h4>💊 Current Medications</h4>
            {snapshot.dynamic_data.current_medications.map((med, idx) => (
              <div key={idx} className="med-item">
                <strong>{med.name} {med.dose}</strong>
                <p>{med.frequency}</p>
                <span className="data-meta">
                  Since: {med.start_date} | Source: {med.source_system}
                </span>
              </div>
            ))}
          </div>

          <div className="data-section">
            <h4>🧬 Recent Labs</h4>
            {snapshot.dynamic_data.recent_labs.map((lab, idx) => (
              <div key={idx} className={`lab-item ${lab.status.toLowerCase()}`}>
                <strong>{lab.test_name}:</strong> {lab.value} {lab.unit}
                <br />
                <span className="data-meta">
                  Normal: {lab.reference_range} | Date: {lab.date}
                </span>
              </div>
            ))}
          </div>

          {snapshot.dynamic_data.recent_diagnoses && snapshot.dynamic_data.recent_diagnoses.length > 0 && (
            <div className="data-section">
              <h4>📋 Recent Diagnoses</h4>
              {snapshot.dynamic_data.recent_diagnoses.map((dx, idx) => (
                <div key={idx} className="dx-item">
                  <strong>{dx.name}</strong>
                  <br />
                  <span className="data-meta">By: {dx.provider} | Date: {dx.date}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* QUICK ACTIONS */}
      <div className="quick-actions">
        <button onClick={onHistory} className="btn-secondary">📜 View Full History</button>
        <button onClick={onEmergency} className="btn-danger">🚨 Emergency Mode</button>
        <button className="btn-secondary">📄 Print Summary</button>
      </div>

      <div className="data-footer">
        Last updated: {new Date().toLocaleString()}
      </div>
    </div>
  )
}
