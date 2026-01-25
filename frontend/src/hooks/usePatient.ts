import { useState, useCallback } from 'react'
import { PatientSnapshot } from '@/types'
import { patientService } from '@/services/api'

export function usePatient() {
  const [snapshot, setSnapshot] = useState<PatientSnapshot | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchSnapshot = useCallback(async (patientId: string) => {
    setLoading(true)
    setError(null)
    try {
      const data = await patientService.getSnapshot(patientId)
      setSnapshot(data)
    } catch (err) {
      setError('Failed to fetch patient snapshot')
    } finally {
      setLoading(false)
    }
  }, [])

  return {
    snapshot,
    loading,
    error,
    fetchSnapshot,
  }
}
