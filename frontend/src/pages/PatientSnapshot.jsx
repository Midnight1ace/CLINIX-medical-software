import { useState } from 'react'
import { User, Calendar, Activity, Droplet, AlertTriangle, Pill, Heart, FileText } from 'lucide-react'
import FileUpload from './FileUpload'
import FileBrowser from './FileBrowser'

function PatientSnapshot({ token, userInfo, patient, onBack, onEmergencyMode, onViewAISummary, onLogout }) {
  const [showFileBrowser, setShowFileBrowser] = useState(false)
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
            <button onClick={() => setShowFileBrowser(true)} className="btn-secondary">📁 Browse Files</button>
            <button onClick={onLogout} className="btn-secondary">Logout</button>
          </div>
        </div>
      </header>

      <div className="content">
        {/* Medical ID Card */}
        <div className="rounded-xl shadow-lg border-l-8 border-blue-500 bg-white overflow-hidden mb-8">
          <div className="bg-blue-50 p-4 flex items-center justify-between border-b border-blue-100">
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-full bg-blue-100 text-blue-600">
                <User className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-blue-900">Patient Medical ID</h2>
                <p className="text-sm text-gray-600 font-medium">{demographics.name}</p>
              </div>
            </div>
            {stable_data.blood_type && (
              <div className="flex items-center space-x-2 bg-white px-3 py-1 rounded-full shadow-sm border border-gray-200">
                <Droplet className="w-4 h-4 text-red-500" />
                <span className="font-bold text-gray-800">{stable_data.blood_type}</span>
              </div>
            )}
          </div>

          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <div className="flex items-center space-x-3 bg-gray-50 p-3 rounded-lg">
                <User className="w-5 h-5 text-gray-600" />
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider">Patient ID</p>
                  <p className="font-semibold text-gray-800">{patient.patient_id}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3 bg-gray-50 p-3 rounded-lg">
                <Calendar className="w-5 h-5 text-gray-600" />
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider">Date of Birth</p>
                  <p className="font-semibold text-gray-800">{demographics.date_of_birth}</p>
                </div>
              </div>

              <div className="flex items-center space-x-3 bg-gray-50 p-3 rounded-lg">
                <Activity className="w-5 h-5 text-gray-600" />
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider">Age</p>
                  <p className="font-semibold text-gray-800">{demographics.age} years</p>
                </div>
              </div>

              <div className="flex items-center space-x-3 bg-gray-50 p-3 rounded-lg">
                <User className="w-5 h-5 text-gray-600" />
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider">Gender</p>
                  <p className="font-semibold text-gray-800">{demographics.gender}</p>
                </div>
              </div>
            </div>

            <div className="flex flex-wrap gap-3">
              <button
                onClick={onEmergencyMode}
                className="flex items-center space-x-2 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-semibold transition-colors duration-200"
              >
                <AlertTriangle className="w-5 h-5" />
                <span>Emergency Mode</span>
              </button>
              <button
                onClick={onViewAISummary}
                className="flex items-center space-x-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold transition-colors duration-200"
              >
                <FileText className="w-5 h-5" />
                <span>AI Summary</span>
              </button>
            </div>
          </div>
        </div>

        {critical_alerts && critical_alerts.length > 0 && (
          <div className="rounded-xl shadow-lg border-l-8 border-red-500 bg-white overflow-hidden mb-8">
            <div className="bg-red-50 p-4 border-b border-red-100">
              <div className="flex items-center space-x-3">
                <div className="p-2 rounded-full bg-red-100 text-red-600">
                  <AlertTriangle className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-bold text-red-900">Critical Alerts</h3>
              </div>
            </div>
            <div className="p-6">
              {critical_alerts.map((alert, idx) => (
                <div key={idx} className="bg-red-50 text-red-800 px-4 py-3 rounded-lg mb-3 border border-red-100">
                  <div className="flex items-start">
                    <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
                    <div>
                      <p className="font-semibold">{alert.message}</p>
                      <p className="text-sm text-red-600 mt-1">Severity: {alert.severity}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="rounded-xl shadow-lg border-l-8 border-green-500 bg-white overflow-hidden">
            <div className="bg-green-50 p-4 border-b border-green-100">
              <div className="flex items-center space-x-3">
                <div className="p-2 rounded-full bg-green-100 text-green-600">
                  <Heart className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-green-900">Stable Medical Data</h3>
                  <p className="text-sm text-gray-600">Rarely changes - Life critical</p>
                </div>
              </div>
            </div>
            <div className="p-6">

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
         </div>

          <div className="rounded-xl shadow-lg border-l-8 border-purple-500 bg-white overflow-hidden">
            <div className="bg-purple-50 p-4 border-b border-purple-100">
              <div className="flex items-center space-x-3">
                <div className="p-2 rounded-full bg-purple-100 text-purple-600">
                  <Activity className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-purple-900">Current Clinical Status</h3>
                  <p className="text-sm text-gray-600">Timestamped and frequently updated</p>
                </div>
              </div>
            </div>
            <div className="p-6">

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

        <div className="mt-8 rounded-xl shadow-lg border-l-8 border-cyan-500 bg-white overflow-hidden">
          <div className="bg-cyan-50 p-4 border-b border-cyan-100">
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-full bg-cyan-100 text-cyan-600">
                <FileText className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-cyan-900">Patient Documents</h3>
            </div>
          </div>
          <div className="p-6">
            <FileUpload token={token} patientId={patient.patient_id} />
          </div>
        </div>
      </div>

      {showFileBrowser && (
        <FileBrowser
          token={token}
          onFileSelect={() => setShowFileBrowser(false)}
          onClose={() => setShowFileBrowser(false)}
        />
      )}
    </div>
  )
}

export default PatientSnapshot