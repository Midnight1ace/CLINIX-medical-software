/// <reference types="vite/client" />
import axios from 'axios'
import { PatientSnapshot } from '@/types'
import { useAuthStore } from '@/store/authStore'

const API_BASE_URL = (import.meta.env.VITE_API_URL as string) || 'http://localhost:8000/api/v1'

const client = axios.create({
  baseURL: API_BASE_URL,
})

// Add token to requests
client.interceptors.request.use((config) => {
  const { token } = useAuthStore()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const patientService = {
  search: async (method: string, value: string) => {
    const response = await client.get('/patients/search', { params: { method, value } })
    return response.data
  },

  getSnapshot: async (patientId: string): Promise<PatientSnapshot> => {
    const response = await client.get(`/patients/${patientId}/snapshot`)
    return response.data
  },

  getEmergency: async (patientId: string) => {
    const response = await client.get(`/patients/${patientId}/emergency`)
    return response.data
  },

  getHistory: async (patientId: string, filters?: any) => {
    const response = await client.get(`/patients/${patientId}/history`, { params: filters })
    return response.data
  },

  getAISummary: async (patientId: string) => {
    const response = await client.get(`/patients/${patientId}/ai-summary`)
    return response.data
  },

  getDocument: async (documentId: string) => {
    const response = await client.get(`/records/document/${documentId}`)
    return response.data
  },
}

export default client
