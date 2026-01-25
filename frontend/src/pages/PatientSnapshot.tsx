import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { PatientSnapshot, Alert } from '@/types'
import { patientService } from '@/services/api'
import PatientHeader from '@/components/PatientHeader'
import AlertBanner from '@/components/AlertBanner'
import StableData from '@/components/StableData'
import DynamicData from '@/components/DynamicData'
import LoadingState from '@/components/LoadingState'
import '../styles/components.css'

export default function PatientSnapshotPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [snapshot, setSnapshot] = useState<PatientSnapshot | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [criticalAlerts, setCriticalAlerts] = useState<Alert[]>([])

  useEffect(() => {
    if (!id) return

    const fetchSnapshot = async () => {
      try {
        const data = await patientService.getSnapshot(id)
        setSnapshot(data)

        // Filter critical alerts
        const critical = data.alerts.filter((a: Alert) => a.severity === 'CRITICAL')
        setCriticalAlerts(critical)
      } catch (err) {
        setError('Failed to load patient snapshot')
      } finally {
        setLoading(false)
      }
    }

    fetchSnapshot()
  }, [id])

  if (loading) return <LoadingState />
  if (error) return <div className="error-message">{error}</div>
  if (!snapshot) return <div>Patient not found</div>

  return (
    <div className="patient-snapshot">
      <PatientHeader patient={snapshot.patient} />

      {criticalAlerts.length > 0 && <AlertBanner alerts={criticalAlerts} />}

      <div className="snapshot-layout">
        <div className="stable-section">
          <StableData
            bloodType={snapshot.stable_data.blood_type?.value}
            allergies={snapshot.stable_data.allergies.map(a => `${a.substance} (${a.severity})`).join(', ')}
            conditions={snapshot.stable_data.chronic_conditions.map(c => c.name).join(', ')}
          />
        </div>

        <div className="dynamic-section">
          <DynamicData records={[]} />
        </div>
      </div>

      <div className="action-buttons">
        <button onClick={() => navigate(`/patient/${id}/history`)}>Full History</button>
        <button onClick={() => navigate(`/patient/${id}/ai-summary`)}>AI Summary</button>
        <button onClick={() => navigate(`/patient/${id}/emergency`)} className="btn-emergency">
          Emergency Mode
        </button>
        <button onClick={() => navigate('/search')}>New Search</button>
      </div>
    </div>
  )
}
