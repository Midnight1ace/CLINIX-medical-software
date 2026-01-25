# Deployment Guide

## Prerequisites

- Docker & Docker Compose
- PostgreSQL 13+
- Python 3.11+
- Node.js 18+

## Backend Deployment

```bash
cd backend
pip install -r requirements.txt
python main.py
```

## Frontend Deployment

```bash
cd frontend
npm install
npm run build
npm run preview
```

## Docker Deployment

```bash
docker-compose -f backend/docker/docker-compose.yml up
```

## Environment Variables

See `.env.example` files in backend and frontend directories.

## Production Checklist

- [ ] Configure TLS/SSL
- [ ] Set up database backups
- [ ] Configure monitoring
- [ ] Set up log aggregation
- [ ] Configure CDN
- [ ] Run security audit
- [ ] Load testing
- [ ] Compliance validation
