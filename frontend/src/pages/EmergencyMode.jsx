import { useState, useEffect } from 'react'

const API_BASE = 'http://localhost:8000'

function EmergencyMode({ token, patient, onExit }) {
  const [emergencyData, setEmergencyData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadEmergencyData = async () => {
      try {
        const response = await fetch(
          `${API_BASE}/api/v1/patients/${patient.patient_id}/emergency`,
          {
            headers: { 'Authorization': `Bearer ${token}` }
          }
        )

        if (!response.ok) {
          throw new Error('Failed to load emergency data')
        }

        const data = await response.json()
        setEmergencyData(data)
      } catch (err) {
        console.error('Error loading emergency data:', err)
      } finally {
        setLoading(false)
      }
    }

    loadEmergencyData()
  }, [token, patient.patient_id])

  if (loading) {
    return <div className="emergency-container"><p>Loading emergency data...</p></div>
  }

  if (!emergencyData) {
    return <div className="emergency-container"><p>Error loading emergency data</p></div>
  }

  return (
    <div className="emergency-container">
      <div className="emergency-header">
        <h1>🚨 EMERGENCY MODE ACTIVE</h1>
        <div className="emergency-patient-info">
          <p><strong>Patient:</strong> {emergencyData.patient_name}</p>
          <p><strong>ID:</strong> {emergencyData.patient_id}</p>
          <p><strong>DOB:</strong> {emergencyData.date_of_birth} (Age: {emergencyData.age})</p>
        </div>
      </div>

      <div className="emergency-content">
        <div className="emergency-section blood-type-section">
          <h2>🩸 BLOOD TYPE</h2>
          <p className="emergency-value-large">{emergencyData.blood_type}</p>
        </div>

        <div className="emergency-section allergies-section">
          <h2>⚠️ CRITICAL ALLERGIES</h2>
          {emergencyData.critical_allergies.length > 0 ? (
            emergencyData.critical_allergies.map((allergy, idx) => (
              <div key={idx} className="emergency-allergy">
                <p className="emergency-value">{allergy.substance}</p>
                <p>Severity: {allergy.severity}</p>
                <p>Reaction: {allergy.reaction}</p>
              </div>
            ))
          ) : (
            <p className="emergency-value">No known critical allergies</p>
          )}
        </div>

        <div className="emergency-section conditions-section">
          <h2>❤️ CHRONIC CONDITIONS</h2>
          {emergencyData.chronic_conditions.length > 0 ? (
            emergencyData.chronic_conditions.map((condition, idx) => (
              <div key={idx} className="emergency-condition">
                <p className="emergency-value">{condition.condition}</p>
                <p>Status: {condition.status}</p>
              </div>
            ))
          ) : (
            <p className="emergency-value">No chronic conditions recorded</p>
          )}
        </div>

        <div className="emergency-section medications-section">
          <h2>💊 CURRENT MEDICATIONS</h2>
          {emergencyData.current_medications.length > 0 ? (
            emergencyData.current_medications.map((med, idx) => (
              <div key={idx} className="emergency-medication">
                <p className="emergency-value">{med.name} ({med.dose})</p>
                <p>{med.frequency}</p>
              </div>
            ))
          ) : (
            <p className="emergency-value">No current medications</p>
          )}
        </div>

        {emergencyData.implants_devices.length > 0 && (
          <div className="emergency-section devices-section">
            <h2>🔧 IMPLANTS/DEVICES</h2>
            {emergencyData.implants_devices.map((device, idx) => (
              <div key={idx} className="emergency-device">
                <p className="emergency-value">{device.type}</p>
                <p>{device.model || 'N/A'}</p>
                <p>Implanted: {device.date_implanted}</p>
              </div>
            ))}
          </div>
        )}

        {emergencyData.recent_vitals.length > 0 && (
          <div className="emergency-section vitals-section">
            <h2>🧬 RECENT VITALS</h2>
            {emergencyData.recent_vitals.map((vital, idx) => (
              <div key={idx} className="emergency-vital">
                <p className="emergency-value">{vital.test_name}: {vital.value}</p>
                <p>{vital.date}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="emergency-footer">
        <button onClick={onExit} className="btn-emergency-exit">
          Exit Emergency Mode
        </button>
      </div>
    </div>
  )
}

export default EmergencyMode
