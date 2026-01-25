# Login Fix - Complete Guide

## What Was Fixed

### 1. **No Demo User in Database** ✅
- Created a demo user script that added the demo credentials to the database
- Demo user created: `demo@hospital.local` / `demo123`
- User is stored as a Doctor role with full credentials

### 2. **CORS Configuration** ✅
- Updated backend CORS to allow Vite dev server on port 5173
- CORS now accepts both `http://localhost:3000` and `http://localhost:5173`
- File: `backend/main.py`

### 3. **Frontend Environment Variables** ✅
- Created `.env.local` in frontend directory
- API URL set to `/api` to use Vite proxy
- Vite proxy forwards `/api` requests to `http://localhost:5000`
- This avoids CORS issues during development

### 4. **Vite Configuration** ✅
- Updated port from 3000 to 5173 (actual Vite dev server port)
- Proxy configuration working correctly
- API requests are forwarded through Vite's proxy

## How to Login Now

1. **Open Frontend**: http://localhost:5173/
2. **Enter Credentials**:
   - Email: `demo@hospital.local`
   - Password: `demo123`
3. **Click Login**

## Files Modified

- `backend/main.py` - Updated CORS configuration
- `frontend/vite.config.ts` - Updated port to 5173
- `frontend/.env.local` - Created with correct API URL
- `backend/create_demo_user.py` - Script to create demo user

## API Testing

Backend login endpoint is working correctly (verified with test):
```
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "email": "demo@hospital.local",
  "password": "demo123"
}
```

Returns:
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "DOC_001",
    "email": "demo@hospital.local",
    "first_name": "Demo",
    "last_name": "Doctor",
    "role": "doctor",
    "active": true
  }
}
```

## Running the Application

### Terminal 1 - Backend
```bash
cd backend
python main.py
```
Backend runs on: http://localhost:5000

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:5173

## Troubleshooting

If login still doesn't work:

1. **Check backend is running**: Visit http://localhost:5000/health
2. **Check database**: The SQLite database file should be at `backend/patient_records.db`
3. **Check network tab**: Open browser DevTools → Network tab and look for `/api/auth/login` requests
4. **Check console**: Look for any error messages in browser console (F12)
5. **Restart servers**: Kill both servers and restart them fresh

## Next Steps

After successful login:
1. Frontend will redirect to `/search` (Patient Search page)
2. You can search for patients
3. Navigate through patient records, snapshots, and AI summaries
4. All data is managed by the Flask backend

---

**Status**: ✅ Login flow is now fully configured and working!
