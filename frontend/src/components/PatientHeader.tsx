import { Patient } from '@/types'

interface PatientHeaderProps {
  patient: Patient
}

export default function PatientHeader({ patient }: PatientHeaderProps) {
  const age = new Date().getFullYear() - new Date(patient.date_of_birth).getFullYear()

  return (
    <div className="patient-header">
      <div className="patient-info">
        <h1>{patient.first_name} {patient.last_name}</h1>
        <div className="patient-details">
          <span>ID: {patient.id}</span>
          <span>Age: {age}</span>
          <span>DOB: {patient.date_of_birth}</span>
          <span>Gender: {patient.gender}</span>
        </div>
      </div>
    </div>
  )
}
