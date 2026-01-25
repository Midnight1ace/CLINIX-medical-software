import React from 'react'
import axios from 'axios'

export default function PatientSearch({ token, onPatientSelected }) {
  const [searchMethod, setSearchMethod] = React.useState('PATIENT_ID')
  const [searchValue, setSearchValue] = React.useState('PAT_987654')
  const [results, setResults] = React.useState(null)
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState('')

  const handleSearch = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await axios.get('http://localhost:8000/api/v1/patients/search', {
        params: { method: searchMethod, value: searchValue },
        headers: { Authorization: `Bearer ${token}` }
      })
      setResults(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Search failed')
      setResults(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="patient-search">
      <div className="search-card">
        <h2>🔍 Find Patient</h2>

        <form onSubmit={handleSearch}>
          <div className="form-group">
            <label>Search Method:</label>
            <select value={searchMethod} onChange={(e) => setSearchMethod(e.target.value)}>
              <option value="PATIENT_ID">Patient ID</option>
              <option value="PARTIAL_NAME">Partial Name</option>
              <option value="NATIONAL_ID">National ID</option>
            </select>
          </div>

          <div className="form-group">
            <label>Search Value:</label>
            <input
              type="text"
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              placeholder="Enter search value"
              disabled={loading}
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Searching...' : '🔍 Search'}
          </button>
        </form>

        {error && <div className="error-message">❌ {error}</div>}

        {results && results.status === 'NOT_FOUND' && (
          <div className="warning-message">⚠️ No patients found</div>
        )}

        {results && results.patients && results.patients.length > 0 && (
          <div className="results">
            <h3>Search Results ({results.count})</h3>
            {results.patients.map((patient) => (
              <div key={patient.patient_id} className="patient-card">
                <div className="patient-info">
                  <h4>{patient.name}</h4>
                  <p>ID: {patient.patient_id} | DOB: {patient.date_of_birth} | Age: {patient.age}</p>
                  <p>Blood Type: {patient.blood_type} | Status: {patient.status}</p>
                </div>
                <button
                  onClick={() => onPatientSelected(patient)}
                  className="btn-select"
                >
                  SELECT →
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
