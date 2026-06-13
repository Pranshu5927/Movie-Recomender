# Phase 2: Containerization (Docker)

**Goal**: Dockerize the backend, frontend, and database so the entire application runs consistently in containers.

**Time**: ~2-3 hours (including testing)

**What You'll Have at the End**:
- Backend running in a Docker container on port 8000
- Frontend running in a Docker container on port 3000
- PostgreSQL database in a Docker container on port 5432
- All services talking to each other
- Local testing works identically to production

---

## What We Created

### Files Created
| File | Purpose |
|------|---------|
| `backend/Dockerfile` | Instructions to build backend Docker image |
| `frontend-react/Dockerfile` | Instructions to build frontend Docker image (multi-stage) |
| `frontend-react/nginx.conf` | Nginx config to serve React and proxy API calls |
| `docker-compose.yml` | Orchestrates all 3 services locally |
| `backend/.dockerignore` | Excludes unnecessary files from Docker image |
| `frontend-react/.dockerignore` | Excludes unnecessary files from Docker image |
| `.env.example` | Template for environment variables |

### Architecture

```
Your Laptop
│
├─ Docker Container 1: Backend (FastAPI + Python)
│  └─ Port 8000
│
├─ Docker Container 2: Frontend (React + Nginx)
│  └─ Port 3000
│  └─ Proxies /api → Backend:8000
│
└─ Docker Container 3: PostgreSQL Database
   └─ Port 5432
   └─ Stores all data
```

---

## Step 1: Verify Docker Installation

### 1.1 Check Docker Is Installed
```bash
docker --version
# Expected: Docker version 24.x.x or higher

docker-compose --version
# Expected: Docker Compose version 2.x.x or higher
```

If not installed:
- Windows/Mac: Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Linux: `sudo apt install docker.io docker-compose`

### 1.2 Start Docker Engine
- **Windows/Mac**: Open Docker Desktop app (wait for it to say "Docker is running")
- **Linux**: `sudo systemctl start docker`

---

## Step 2: Set Up Environment Variables

### 2.1 Copy .env.example to .env
```bash
cd path/to/Movie-Recommender
cp .env.example .env
```

### 2.2 Edit .env with Your Keys
Open `.env` in your text editor and fill in:

```
DB_USER=postgres
DB_PASSWORD=postgres  # For local dev only! Change in production
DB_NAME=movie_recommender
SECRET_KEY=dev-secret-key-change-in-production
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE  # Get from https://platform.openai.com/api-keys
```

**Important**: Never commit `.env` to GitHub (it's in `.gitignore`)

---

## Step 3: Build and Start Services

### 3.1 Build Docker Images
```bash
docker-compose build
```

**What's happening:**
- Downloads Python 3.10 slim (backend base image)
- Downloads Node.js 18 (frontend base image)
- Downloads Postgres 15 (database image)
- Installs Python dependencies from `requirements.txt`
- Installs Node dependencies from `package.json`
- Builds React app with Vite
- Creates Nginx container with built React app

**Time**: 5-15 minutes first time (faster on subsequent builds)

### 3.2 Start All Services
```bash
docker-compose up
```

**What's happening:**
- Starts PostgreSQL container → Available on localhost:5432
- Waits for database to be healthy (≈5 sec)
- Starts Backend container → Available on localhost:8000
- Starts Frontend container → Available on localhost:3000

**Expected Output:**
```
movie-recommender-db        | LOG: database system is ready to accept connections
movie-recommender-backend   | INFO:     Uvicorn running on http://0.0.0.0:8000
movie-recommender-frontend  | ... (nginx starting)
```

**Leave this running.** Open a new terminal for testing.

---

## Step 4: Test the Application

### 4.1 Test Backend is Running
```bash
# In a new terminal
curl http://localhost:8000/

# Expected response:
# {"message":"Movie Recommender API is running"}
```

### 4.2 Test Frontend is Running
```bash
# Open browser to: http://localhost:3000
# You should see the Movie Recommender homepage
```

### 4.3 Test Database Connection
```bash
# In a new terminal
docker exec movie-recommender-db psql -U postgres -d movie_recommender -c "SELECT version();"

# Expected: PostgreSQL version info
```

### 4.4 Test API Endpoints

**Health check:**
```bash
curl http://localhost:8000/
```

**List movies:**
```bash
curl http://localhost:8000/movies
```

**Sign up (create account):**
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Expected: {"user_id": 1, "username": "testuser"}
```

### 4.5 Test Seed Data

If you haven't seeded the database yet, you need to do it inside the container:

```bash
# In the backend container, run seed scripts
docker exec movie-recommender-backend python scripts/seed_movies.py
docker exec movie-recommender-backend python scripts/seed_ratings.py
docker exec movie-recommender-backend python scripts/seed_tags.py
docker exec movie-recommender-backend python scripts/generate_movie_embeddings.py
```

**Note**: Generating embeddings takes 3-5 minutes. Grab coffee ☕

---

## Step 5: Common Operations

### 5.1 Stop All Services
```bash
# Stop and keep containers
Ctrl+C  # (in the terminal running docker-compose up)

# Or in another terminal:
docker-compose stop
```

### 5.2 Start Again (After Stopping)
```bash
docker-compose up
```

### 5.3 View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### 5.4 Access Backend Container Shell
```bash
docker exec -it movie-recommender-backend bash
# Now you're inside the container, can run Python commands
```

### 5.5 Access Database
```bash
docker exec -it movie-recommender-db psql -U postgres -d movie_recommender
# Now connected to PostgreSQL, can run SQL queries
```

### 5.6 Rebuild After Code Changes
```bash
# If you change Python code:
docker-compose down
docker-compose build
docker-compose up

# Or (faster, only rebuilds backend):
docker-compose up --build backend
```

### 5.7 Clean Up Everything
```bash
# Stop and remove containers
docker-compose down

# Remove volumes (WARNING: deletes database)
docker-compose down -v

# Clean up all Docker resources (careful!)
docker system prune
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Docker daemon is not running" | Start Docker Desktop (Windows/Mac) or `sudo systemctl start docker` (Linux) |
| Port 3000/8000/5432 already in use | Change ports in `docker-compose.yml`: `"3001:80"` instead of `"3000:80"` |
| Backend container exits immediately | Check logs: `docker-compose logs backend`. Usually missing OPENAI_API_KEY |
| Cannot connect to database | Wait 5-10 seconds for postgres to start. Check health: `docker-compose ps` |
| Frontend shows blank page | Check browser console (F12) for errors. Check nginx proxy config. |
| `OPENAI_API_KEY not set` error | Add it to `.env` file: `OPENAI_API_KEY=sk-proj-...` |
| Database data lost after `docker-compose down -v` | Normal behavior. Database is in a volume. Use `down` without `-v` to keep data. |
| Container won't rebuild after code changes | Try `docker-compose build --no-cache backend` |

---

## What's Happening Under the Hood

### Backend Dockerfile Explanation
```dockerfile
FROM python:3.10-slim              # Use lightweight Python image
RUN apt-get install gcc ...        # Install build tools for packages
COPY requirements.txt .            # Copy dependencies file
RUN pip install ...                # Install Python packages
COPY backend/ .                    # Copy your code
EXPOSE 8000                        # Open port 8000
CMD ["uvicorn", ...]               # Run FastAPI
```

### Frontend Dockerfile Explanation (Multi-Stage Build)
```dockerfile
# Stage 1: Build
FROM node:18-slim as builder       # Download Node.js
RUN npm ci                         # Install dependencies
RUN npm run build                  # Build React app → creates dist/

# Stage 2: Serve
FROM nginx:alpine                  # Download Nginx
COPY --from=builder dist/ /html    # Copy built app from stage 1
EXPOSE 80                          # Open port 80
CMD ["nginx", ...]                 # Run Nginx
```

**Why multi-stage?**
- Stage 1 is 400+ MB (Node.js + build tools)
- Stage 2 uses only the 20 MB built output
- Final image: ~50 MB instead of 400+ MB
- Faster to push to AWS later

### docker-compose.yml Explanation
```yaml
services:
  postgres:              # Service 1: Database
    image: postgres:15   # Public image from Docker Hub
    ports: "5432:5432"  # Port mapping: container:host
    volumes: postgres_data  # Persistent storage

  backend:              # Service 2: FastAPI
    build: backend/     # Build using backend/Dockerfile
    depends_on: postgres  # Start postgres first
    environment: ...    # Pass .env variables

  frontend:             # Service 3: React
    build: frontend/    # Build using frontend/Dockerfile
    depends_on: backend # Start backend first
```

---

## Success Checklist

- ✅ `docker-compose up` starts all 3 services without errors
- ✅ Backend responds on http://localhost:8000
- ✅ Frontend loads on http://localhost:3000
- ✅ Can sign up, log in (POST /auth/signup, /auth/login)
- ✅ Can get recommendations (GET /recommendations)
- ✅ Database has seeded movies
- ✅ No crashes or connection errors in logs
- ✅ Stopped with `Ctrl+C`, can restart with `docker-compose up`

---

## Key Concepts Learned

1. **Docker Images**: Blueprint (like a template) for containers
2. **Docker Containers**: Running instance of an image
3. **Dockerfile**: Instructions to build an image
4. **docker-compose**: Tool to manage multiple containers together
5. **Multi-stage builds**: Optimize final image size
6. **Health checks**: Ensure services are ready before others depend on them
7. **Volumes**: Persistent storage that survives container restarts
8. **Networks**: Internal Docker network so containers talk to each other

---

## Next Steps

✅ Verify everything works locally with `docker-compose up`  
✅ You can see logs with `docker-compose logs -f`  
✅ When satisfied, stop with `Ctrl+C`  

**Next Phase**: Phase 3 — GitHub Actions (automated testing + building)
- Create `.github/workflows/ci-cd.yml`
- Push code → GitHub Actions runs tests → builds Docker images
- Test with a PR

---

## Quick Reference Commands

```bash
# Start everything
docker-compose up

# Rebuild and start
docker-compose up --build

# Stop everything
Ctrl+C

# View logs
docker-compose logs -f

# Access backend shell
docker exec -it movie-recommender-backend bash

# Access database
docker exec -it movie-recommender-db psql -U postgres

# Clean everything
docker-compose down -v
```
