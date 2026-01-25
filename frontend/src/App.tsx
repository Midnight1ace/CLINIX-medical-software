import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'

// Pages
import Login from '@/pages/Login'
import PatientSearch from '@/pages/PatientSearch'
import PatientSnapshot from '@/pages/PatientSnapshot'
import PatientHistory from '@/pages/PatientHistory'
import AISummary from '@/pages/AISummary'
import EmergencyMode from '@/pages/EmergencyMode'

// Components
import Header from '@/components/Header'

function App() {
  const { token } = useAuthStore()

  return (
    <Router>
      <div className="app">
        {token && <Header />}
        <main>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/search"
              element={token ? <PatientSearch /> : <Navigate to="/login" />}
            />
            <Route
              path="/patient/:id/snapshot"
              element={token ? <PatientSnapshot /> : <Navigate to="/login" />}
            />
            <Route
              path="/patient/:id/history"
              element={token ? <PatientHistory /> : <Navigate to="/login" />}
            />
            <Route
              path="/patient/:id/ai-summary"
              element={token ? <AISummary /> : <Navigate to="/login" />}
            />
            <Route
              path="/patient/:id/emergency"
              element={token ? <EmergencyMode /> : <Navigate to="/login" />}
            />
            <Route path="/" element={token ? <Navigate to="/search" /> : <Navigate to="/login" />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
