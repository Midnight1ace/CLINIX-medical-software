# API Reference

Complete API endpoint documentation.

## Authentication

### POST /auth/login
Login with credentials

### POST /auth/logout
Logout current session

## Patients

### GET /patients/search
Search for patients

### GET /patients/{id}/snapshot
Get patient snapshot

### GET /patients/{id}/history
Get full medical history

### GET /patients/{id}/ai-summary
Get AI-generated summary

## Pharmacy

### GET /pharmacy/patients/{id}/medications
Get patient medications

## Clinic

### GET /clinic/patients/{id}/appointments
Get appointments
