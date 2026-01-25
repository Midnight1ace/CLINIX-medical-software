import { create } from 'zustand'
import { Patient, PatientSnapshot } from '@/types'

interface PatientState {
  patient: Patient | null
  snapshot: PatientSnapshot | null
  setPatient: (patient: Patient) => void
  setSnapshot: (snapshot: PatientSnapshot) => void
  clearPatient: () => void
}

export const usePatientStore = create<PatientState>((set) => ({
  patient: null,
  snapshot: null,

  setPatient: (patient: Patient) => {
    set({ patient })
  },

  setSnapshot: (snapshot: PatientSnapshot) => {
    set({ snapshot, patient: snapshot.patient })
  },

  clearPatient: () => {
    set({ patient: null, snapshot: null })
  },
}))
