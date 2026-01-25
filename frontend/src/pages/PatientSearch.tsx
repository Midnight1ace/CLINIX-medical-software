import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Patient } from '@/types'
import { patientService } from '@/services/api'
import '../styles/components.css'

export default function PatientSearch() {
  const [searchQuery, setSearchQuery] = useState('')
  const [results, setResults] = useState<Patient[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    setLoading(true)
    setError('')

    try {
      const data = await patientService.search('PATIENT_ID', searchQuery)
      if (data.patients) {
        setResults(data.patients)
      } else {
        setResults([])
        setError('No patients found')
      }
    } catch (err) {
      setError('Search failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="patient-search">
      <h1>Patient Search</h1>

      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Enter Patient ID, Name, or National ID"
          autoFocus
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}

      <div className="search-results">
        {results.map((patient) => (
          <div key={patient.patient_id} className="patient-card">
            <h3>
              {patient.name}
            </h3>
            <p>ID: {patient.patient_id}</p>
            <p>Age: {patient.age}</p>
            <button onClick={() => navigate(`/patient/${patient.patient_id}/snapshot`)}>
              View Snapshot
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
