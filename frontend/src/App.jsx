import React from 'react'
import './App.css'
import Login from './pages/Login'
import PatientSearch from './pages/PatientSearch'
import PatientSnapshot from './pages/PatientSnapshot'
import EmergencyMode from './pages/EmergencyMode'
import AISummary from './pages/AISummary'

export default function App() {
  const [currentPage, setCurrentPage] = React.useState('login')
  const [token, setToken] = React.useState(localStorage.getItem('token'))
  const [user, setUser] = React.useState(JSON.parse(localStorage.getItem('user') || '{}'))
  const [selectedPatient, setSelectedPatient] = React.useState(null)

  const handleLogin = (data) => {
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify({ name: data.name, role: data.role, user_id: data.user_id }))
    setToken(data.access_token)
    setUser({ name: data.name, role: data.role, user_id: data.user_id })
    setCurrentPage('search')
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setToken(null)
    setUser(null)
    setCurrentPage('login')
  }

  const handlePatientSelected = (patient) => {
    setSelectedPatient(patient)
    setCurrentPage('snapshot')
  }

  if (!token) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <h1>🏥 AI-Patient Record Intelligence</h1>
          <p className="subtitle">Doctor-first clinical clarity</p>
        </div>
        <div className="header-right">
          <span>👤 {user.name} ({user.role})</span>
          <button onClick={handleLogout} className="btn-logout">Logout</button>
        </div>
      </header>

      <main className="main-content">
        {currentPage === 'search' && (
          <PatientSearch token={token} onPatientSelected={handlePatientSelected} />
        )}
        {currentPage === 'snapshot' && selectedPatient && (
          <PatientSnapshot
            token={token}
            patient={selectedPatient}
            onEmergency={() => setCurrentPage('emergency')}
            onHistory={() => setCurrentPage('history')}
            onBack={() => setCurrentPage('search')}
          />
        )}
        {currentPage === 'emergency' && selectedPatient && (
          <EmergencyMode
            token={token}
            patient={selectedPatient}
            onBack={() => setCurrentPage('snapshot')}
          />
        )}
        {currentPage === 'ai-summary' && selectedPatient && (
          <AISummary
            token={token}
            patient={selectedPatient}
            onBack={() => setCurrentPage('snapshot')}
          />
        )}
      </main>
    </div>
  )
}
