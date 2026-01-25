# System Architecture

## Overview

This document outlines the complete system architecture for AI-Patient-Record-Intelligence.

## Core Components

### Frontend (React + TypeScript)
- Patient search interface
- Snapshot view for quick clinical overview
- Full history timeline
- AI summary display
- Emergency mode for crisis situations

### Backend (Flask + Python)
- RESTful API for all operations
- Patient data management
- Medical record handling
- AI summary generation
- Audit logging

### Database (PostgreSQL)
- Patient demographics
- Medical records
- Audit logs
- User management

## Data Flow

1. User authenticates
2. Searches for patient
3. Views snapshot (critical data)
4. Can access full history or emergency mode
5. All actions logged for compliance

## Security

- HIPAA-compliant encryption
- GDPR data protection
- JWT authentication
- Comprehensive audit trails
