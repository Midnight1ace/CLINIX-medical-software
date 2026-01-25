/**
 * TypeScript Type Definitions
 */

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'DOCTOR' | 'PHARMACIST' | 'STAFF' | 'ADMIN';
  active: boolean;
}

export interface Patient {
  patient_id: string;
  name: string;
  date_of_birth: string;
  age: number;
  gender: string;
  national_id?: string;
  blood_type?: string;
  last_visit?: string;
  last_provider?: string;
  confidence?: number;
  status?: string;
}

export interface Alert {
  alert_id: string;
  type: string;
  severity: string;
  message: string;
  substance?: string;
  verified?: boolean;
  verified_date?: string;
  action_required?: boolean;
}

export interface MedicalRecord {
  id: string;
  patient_id: string;
  record_type: string;
  title: string;
  description?: string;
  record_date: string;
  source: string;
  verified: boolean;
  is_critical: boolean;
}

export interface PatientSnapshot {
  patient: {
    patient_id: string;
    name: string;
    date_of_birth: string;
    age: number;
    gender: string;
    blood_type?: string;
    status: string;
  };
  alerts: Array<{
    alert_id: string;
    type: string;
    severity: string;
    message: string;
    substance?: string;
    verified?: boolean;
    verified_date?: string;
  }>;
  stable_data: {
    blood_type?: {
      value: string;
      verified_date: string;
      source: string;
    };
    allergies: Array<{
      substance: string;
      severity: string;
      reaction: string;
      verified_date: string;
      source: string;
    }>;
    chronic_conditions: Array<{
      name: string;
      icd_code: string;
      diagnosis_date: string;
      status: string;
      source: string;
    }>;
    implants_devices: Array<{
      type: string;
      manufacturer?: string;
      model?: string;
      implant_date: string;
      location?: string;
      next_checkup?: string;
      notes?: string;
    }>;
  };
  dynamic_data: {
    current_medications: Array<{
      medication_id: string;
      name: string;
      dose: string;
      frequency: string;
      route: string;
      start_date: string;
      prescriber: string;
      source_system: string;
      last_filled?: string;
      refills_remaining?: number;
      days_supply?: number;
    }>;
    recent_labs: Array<{
      lab_id: string;
      test_name: string;
      value: number;
      unit: string;
      reference_range: string;
      status: string;
      date: string;
      lab: string;
      provider: string;
    }>;
    recent_diagnoses: Array<{
      diagnosis_id: string;
      name: string;
      icd_code: string;
      date: string;
      provider: string;
      status: string;
      source: string;
    }>;
    ongoing_treatments: Array<{
      treatment_id: string;
      type: string;
      description: string;
      start_date: string;
      provider: string;
      status: string;
    }>;
  };
  data_sources: {
    last_updated: string;
    medications?: {
      system: string;
      last_sync: string;
    };
    allergies?: {
      system: string;
      last_sync: string;
    };
    labs?: {
      system: string;
      last_sync: string;
    };
    diagnoses?: {
      system: string;
      last_sync: string;
    };
  };
}

export interface AuthResponse {
  success: boolean;
  token?: string;
  user?: User;
  error?: string;
}

export interface ApiError {
  error: string;
  message: string;
  timestamp: string;
  request_id?: string;
}
