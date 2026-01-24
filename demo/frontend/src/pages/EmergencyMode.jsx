import React from 'react'
import axios from 'axios'

export default function EmergencyMode({ token, patient, onBack }) {
  const [emergencyData, setEmergencyData] = React.useState(null)
  const [loading, setLoading] = React.useState(true)

  React.useEffect(() => {
    const fetchEmergency = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/v1/patients/${patient.patient_id}/emergency`,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        setEmergencyData(response.data)
      } finally {
        setLoading(false)
      }
    }
    fetchEmergency()
  }, [patient, token])

  if (loading) return <div className="emergency-loading">Loading emergency data...</div>
  if (!emergencyData) return <div>No data</div>

  return (
    <div className="emergency-container">
      <div className="emergency-header">
        🚨 🚨 🚨 EMERGENCY MODE ACTIVE 🚨 🚨 🚨
      </div>

      <div className="emergency-patient">
        <p>Patient: <strong>{emergencyData.patient.name}</strong></p>
        <p>ID: {emergencyData.patient.patient_id}</p>
        <p>DOB: {emergencyData.patient.date_of_birth} | Age: {emergencyData.patient.age}</p>
      </div>

      <div className="emergency-section blood-type">
        <h2>🩸 BLOOD TYPE</h2>
        <div className="blood-type-value">{emergencyData.blood_type}</div>
      </div>

      <div className="emergency-section critical-allergies">
        <h2>⚠️ CRITICAL ALLERGIES</h2>
        {emergencyData.allergies.map((allergy, idx) => (
          <div key={idx} className="emergency-allergy">
            <div className="allergy-severity">{allergy.severity}</div>
            <div className="allergy-text">
              <strong>{allergy.substance}</strong> - {allergy.reaction}
            </div>
          </div>
        ))}
      </div>

      <div className="emergency-section">
        <h2>❤️ CHRONIC CONDITIONS</h2>
        <div className="conditions-list">
          {emergencyData.chronic_conditions.map((condition, idx) => (
            <div key={idx} className="condition">• {condition}</div>
          ))}
        </div>
      </div>

      <div className="emergency-section">
        <h2>💊 CURRENT MEDICATIONS</h2>
        {emergencyData.current_medications.map((med, idx) => (
          <div key={idx} className="medication">
            • {med.name} {med.dose} ({med.frequency})
          </div>
        ))}
      </div>

      {emergencyData.devices && emergencyData.devices.length > 0 && (
        <div className="emergency-section warning">
          <h2>🏥 DEVICES</h2>
          {emergencyData.devices.map((device, idx) => (
            <div key={idx} className="device-warning">
              <strong>{device.type}</strong>
              <p>{device.notes}</p>
            </div>
          ))}
        </div>
      )}

      <div className="emergency-actions">
        <button onClick={onBack} className="btn-back-emergency">EXIT EMERGENCY MODE</button>
      </div>
    </div>
  )
}
