function PatientSnapshot({ token, userInfo, patient, onBack, onEmergencyMode, onViewAISummary, onLogout }) {
  if (!patient) {
    return <div>Loading...</div>
  }

  const { demographics, critical_alerts, stable_data, dynamic_data } = patient

  return (
    <div className="page-container">
      <header className="page-header">
        <div className="header-content">
          <div className="header-left">
            <button onClick={onBack} className="btn-secondary">← Back to Search</button>
            <h1>Patient Record</h1>
          </div>
          <div className="user-info">
            <span>{userInfo.name} ({userInfo.role})</span>
            <button onClick={onLogout} className="btn-secondary">Logout</button>
          </div>
        </div>
      </header>

      <div className="content">
        <div className="patient-header">
          <div className="patient-info">
            <h2>{demographics.name}</h2>
            <div className="patient-meta">
              <span>ID: {patient.patient_id}</span>
              <span>DOB: {demographics.date_of_birth}</span>
              <span>Age: {demographics.age}</span>
              <span>Gender: {demographics.gender}</span>
              <span>Blood Type: <strong className="blood-type">{stable_data.blood_type}</strong></span>
            </div>
          </div>
          <div className="quick-actions">
            <button onClick={onEmergencyMode} className="btn-emergency">
              🚨 Emergency Mode
            </button>
            <button onClick={onViewAISummary} className="btn-primary">
              AI Summary
            </button>
          </div>
        </div>

        {critical_alerts && critical_alerts.length > 0 && (
          <div className="alert-banner">
            {critical_alerts.map((alert, idx) => (
              <div key={idx} className={`alert alert-${alert.severity.toLowerCase()}`}>
                {alert.message}
              </div>
            ))}
          </div>
        )}

        <div className="snapshot-grid">
          <div className="stable-data-panel">
            <h3>🔒 Stable Medical Data</h3>
            <p className="panel-subtitle">Rarely changes - Life critical</p>

            <div className="data-section">
              <h4>Blood Type</h4>
              <p className="data-value">{stable_data.blood_type}</p>
            </div>

            <div className="data-section">
              <h4>Allergies</h4>
              {stable_data.allergies.map((allergy, idx) => (
                <div key={idx} className={`allergy allergy-${allergy.severity.toLowerCase()}`}>
                  <strong>{allergy.substance}</strong>
                  <p>Severity: {allergy.severity}</p>
                  <p>Reaction: {allergy.reaction}</p>
                  <p className="data-source">Verified: {allergy.verified_date}</p>
                </div>
              ))}
            </div>

            <div className="data-section">
              <h4>Chronic Conditions</h4>
              {stable_data.chronic_conditions.map((condition, idx) => (
                <div key={idx} className="condition">
                  <strong>{condition.condition}</strong>
                  <p>Status: {condition.status}</p>
                  <p>Diagnosed: {condition.diagnosed_date}</p>
                  <p className="data-source">ICD: {condition.icd_code}</p>
                </div>
              ))}
            </div>

            {stable_data.implants_devices.length > 0 && (
              <div className="data-section">
                <h4>Implants/Devices</h4>
                {stable_data.implants_devices.map((device, idx) => (
                  <div key={idx} className="device">
                    <strong>{device.type}</strong>
                    <p>{device.model || 'N/A'}</p>
                    <p>Implanted: {device.date_implanted}</p>
                    <p className="data-source">Location: {device.location || 'N/A'}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="dynamic-data-panel">
            <h3>📊 Current Clinical Status</h3>
            <p className="panel-subtitle">Timestamped and frequently updated</p>

            <div className="data-section">
              <h4>Current Medications</h4>
              {dynamic_data.current_medications.map((med, idx) => (
                <div key={idx} className="medication">
                  <strong>{med.name}</strong> ({med.dose})
                  <p>Frequency: {med.frequency}</p>
                  <p>Prescriber: {med.prescriber}</p>
                  <p className="data-source">Last filled: {med.last_filled} | Refills: {med.refills_remaining}</p>
                </div>
              ))}
            </div>

            <div className="data-section">
              <h4>Recent Labs (Last 7 days)</h4>
              {dynamic_data.recent_labs.map((lab, idx) => (
                <div key={idx} className={`lab-result lab-${lab.status.toLowerCase()}`}>
                  <strong>{lab.test_name}</strong>
                  <p className="lab-value">{lab.value}</p>
                  <p>Reference: {lab.reference_range}</p>
                  <p className="data-source">{lab.date} | {lab.facility}</p>
                </div>
              ))}
            </div>

            <div className="data-section">
              <h4>Recent Diagnoses</h4>
              {dynamic_data.recent_diagnoses.map((diagnosis, idx) => (
                <div key={idx} className="diagnosis">
                  <strong>{diagnosis.diagnosis}</strong>
                  <p>Status: {diagnosis.status}</p>
                  <p>Provider: {diagnosis.provider}</p>
                  <p className="data-source">{diagnosis.date} | {diagnosis.facility}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PatientSnapshot
