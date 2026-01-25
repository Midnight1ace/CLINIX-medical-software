import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { patientService } from '@/services/api'
import LoadingState from '@/components/LoadingState'
import '../styles/components.css'

interface EmergencyData {
  patient: {
    patient_id: string;
    name: string;
    date_of_birth: string;
    age: number;
  };
  blood_type: string;
  allergies: Array<{
    substance: string;
    severity: string;
    reaction: string;
  }>;
  chronic_conditions: string[];
  current_medications: Array<{
    name: string;
    dose: string;
    frequency: string;
  }>;
  devices: Array<{
    type: string;
    notes?: string;
    implant_date?: string;
  }>;
  recent_vitals: {
    blood_pressure?: { value: string; date: string };
    glucose?: { value: string; date: string };
    heart_rate?: { value: string; date: string };
  };
}

export default function EmergencyMode() {
  const { id } = useParams<{ id: string }>()
  const [data, setData] = useState<EmergencyData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!id) return

    const fetchData = async () => {
      try {
        const emergencyData = await patientService.getEmergency(id)
        setData(emergencyData)
      } catch (err) {
        setError('Failed to load emergency data')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [id])

  if (loading) return <LoadingState />
  if (error) return <div className="error-message">{error}</div>
  if (!data) return <div>Patient not found</div>

  return (
    <div className="emergency-mode">
      <div className="emergency-header">
        <h1>{data.patient.name}</h1>
        <p className="patient-id">ID: {data.patient.patient_id}</p>
      </div>

      <div className="emergency-grid">
        <div className="emergency-section">
          <h2>BLOOD TYPE</h2>
          <p className="large-text">{data.blood_type}</p>
        </div>

        <div className="emergency-section critical">
          <h2>ALLERGIES</h2>
          {data.allergies.length > 0 ? (
            data.allergies.map((allergy, index) => (
              <p key={index} className="large-text">
                {allergy.substance} - {allergy.reaction}
              </p>
            ))
          ) : (
            <p>None documented</p>
          )}
        </div>

        <div className="emergency-section">
          <h2>CONDITIONS</h2>
          {data.chronic_conditions.length > 0 ? (
            data.chronic_conditions.map((condition, index) => (
              <p key={index} className="large-text">{condition}</p>
            ))
          ) : (
            <p>None documented</p>
          )}
        </div>

        <div className="emergency-section">
          <h2>CURRENT MEDICATIONS</h2>
          {data.current_medications.length > 0 ? (
            data.current_medications.map((med, index) => (
              <p key={index} className="large-text">
                {med.name} {med.dose} - {med.frequency}
              </p>
            ))
          ) : (
            <p>None documented</p>
          )}
        </div>
      </div>
    </div>
  )
}
