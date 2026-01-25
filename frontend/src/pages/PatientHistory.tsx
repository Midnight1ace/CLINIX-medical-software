import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { MedicalRecord } from '@/types'
import { patientService } from '@/services/api'
import Timeline from '@/components/Timeline'
import LoadingState from '@/components/LoadingState'

export default function PatientHistory() {
  const { id } = useParams<{ id: string }>()
  const [records, setRecords] = useState<MedicalRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!id) return

    const fetchHistory = async () => {
      try {
        const data = await patientService.getHistory(id)
        setRecords(data.history || [])
      } catch (err) {
        setError('Failed to load patient history')
      } finally {
        setLoading(false)
      }
    }

    fetchHistory()
  }, [id])

  if (loading) return <LoadingState />
  if (error) return <div className="error-message">{error}</div>

  return (
    <div className="patient-history">
      <h1>Medical History Timeline</h1>
      <Timeline records={records} />
    </div>
  )
}
