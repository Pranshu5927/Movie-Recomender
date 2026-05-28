# 🚀 Quick Start Reference

## One-Command Quick Start

### Windows PowerShell

```powershell
# Navigate to project
cd "e:\D_drive\Personal Dev\Projects\Habitat\Movie-Recommender"

# Start backend (Terminal 1)
.\Recommender_venv\Scripts\activate
cd backend
python main.py

# Start frontend (Terminal 2)
.\Recommender_venv\Scripts\activate
cd frontend
streamlit run app.py
```

### macOS/Linux Bash

```bash
# Navigate to project
cd ~/path/to/Movie-Recommender

# Start backend (Terminal 1)
source Recommender_venv/bin/activate
cd backend
python main.py

# Start frontend (Terminal 2)
source Recommender_venv/bin/activate
cd frontend
streamlit run app.py
```

## Access Points

- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs
- **Frontend App**: http://localhost:8501

## Demo Workflow

### 1. Create Account
- Go to frontend (http://localhost:8501)
- Click "Sign Up" tab
- Enter: username, email, password
- Click "🎬 Sign Up"

### 2. Login
- Click "Login" tab
- Enter: email, password
- Click "🔓 Login"

### 3. Explore Features
- **Recommendations**: See top movies
- **Search**: Try searching "the" or "movie"
- **Watchlist**: Add some movies
- **Settings**: View profile info

### 4. Rate & Interact
- Rate movies using slider (0.5-5.0 stars)
- Add to watchlist with one click
- Submit ratings for personalization

## Troubleshooting

### Backend Won't Start
```bash
# Check if port is in use
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -i :8000

# Try different port in backend/.env
DATABASE_URL=postgresql://...
PORT=8001
```

### Frontend Won't Connect
```bash
# Verify backend is running
curl http://127.0.0.1:8000

# Check .streamlit/config.toml
# Ensure BACKEND_URL is correct

# Restart streamlit
streamlit run app.py --logger.level=debug
```

### Database Connection Error
```bash
# Check .env file in backend/
# Verify DATABASE_URL is correct
# Ensure PostgreSQL is running
```

### Port 8501 Already in Use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

## File Structure

```
Movie-Recommender/
├── backend/              (Don't modify ✗)
├── frontend/            (Beautiful new version ✓)
│   ├── app.py           (Main Streamlit app - UPDATED)
│   ├── api.py           (API client - ENHANCED)
│   ├── .streamlit/
│   │   └── config.toml  (Theme config - NEW)
│   └── README.md        (Frontend guide - UPDATED)
├── data/                (Datasets)
├── notebooks/           (Analysis)
├── requirements.txt     (Dependencies - UPDATED)
├── SETUP_GUIDE.md       (Complete setup - NEW)
└── FEATURES_SHOWCASE.md (Features list - NEW)
```

## Key Files Changed

### ✅ frontend/app.py
- Complete redesign with professional UI
- Dark theme with gradients
- Tab-based navigation
- Enhanced error handling
- Production-ready styling

### ✅ frontend/api.py
- Better error handling
- Request timeouts
- Improved documentation
- Additional utility functions
- Connection status checks

### ✅ frontend/.streamlit/config.toml
- Custom theme colors
- Performance settings
- Security settings
- UI customization

### ✅ frontend/README.md
- User guide
- Feature documentation
- Setup instructions
- Troubleshooting

### ✅ requirements.txt
- Latest versions specified
- Added missing packages
- Production-ready dependencies

### ✅ New Files
- SETUP_GUIDE.md - Complete deployment guide
- FEATURES_SHOWCASE.md - Feature documentation

## Backend Status (Unchanged)

Backend is solid and not modified:
- ✅ FastAPI server (main.py)
- ✅ Authentication (api/auth.py)
- ✅ Recommendations (api/recommendations.py)
- ✅ Watchlist management (api/watchlist.py)
- ✅ Rating system (api/ratings.py)
- ✅ Movie search (backend/api/movies)
- ✅ Database models (backend/models/)

All backend endpoints remain the same and functional.

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost/movies_db
SECRET_KEY=your_secret_key_here
JWT_EXPIRATION=24
```

### Frontend (optional .env)
```env
BACKEND_URL=http://127.0.0.1:8000
STREAMLIT_PORT=8501
STREAMLIT_SERVER_MAXUPLOADSIZE=500
```

## Testing the APIs

### Test Backend
```bash
# Check if API is running
curl http://127.0.0.1:8000

# Get API docs
curl http://127.0.0.1:8000/docs

# Search movies
curl "http://127.0.0.1:8000/movies/search?query=the"
```

### Test Authentication
```bash
# Signup
curl -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@test.com",
    "password": "pass123"
  }'

# Login
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@test.com",
    "password": "pass123"
  }'
```

## Performance Tips

1. **Backend**: Run on a machine with good specs
2. **Database**: Use PostgreSQL for best performance
3. **Frontend**: Streamlit handles scaling well
4. **Network**: Keep backend and frontend on same network
5. **Caching**: Frontend caches search results in session

## Common Issues

| Issue | Solution |
|-------|----------|
| "Connection refused" | Ensure backend is running |
| "No recommendations" | Rate some movies first |
| "Invalid token" | Login again |
| "500 Server error" | Check backend logs |
| "Timeout" | Verify network connectivity |
| "Database error" | Check PostgreSQL is running |

## Next Steps After Running

1. ✅ Create a test account
2. ✅ Verify login works
3. ✅ Test movie search
4. ✅ Add movies to watchlist
5. ✅ Rate some movies
6. ✅ View recommendations
7. ✅ Test all UI features
8. ✅ Check mobile responsive design

## Deployment Checklist

- [ ] Backend running on production server
- [ ] Database backed up
- [ ] Environment variables set
- [ ] HTTPS/SSL configured
- [ ] Frontend deployed to Streamlit Cloud
- [ ] Backend URL updated in frontend
- [ ] Error logging enabled
- [ ] Monitor system performance

## Support & Documentation

- **Frontend Guide**: `frontend/README.md`
- **Setup Guide**: `SETUP_GUIDE.md`
- **Features List**: `FEATURES_SHOWCASE.md`
- **Backend Docs**: `http://localhost:8000/docs`
- **Streamlit Docs**: https://docs.streamlit.io
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

**Ready to launch! 🎬🚀**

Everything is set up and ready to run. No backend changes were made - only the frontend was beautified!
