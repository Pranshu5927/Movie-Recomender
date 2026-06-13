# Movie Recommender: Productionization Progress

## Overview

**Goal**: Productionize the Movie Recommender application using industry-level MLOps tools and deployment strategies.

**Budget**: $20-30/month on AWS free tier  
**Scope**: Docker → GitHub Actions → AWS ECS (skip Kubernetes for now)  
**Learning Focus**: Deploy-as-you-go approach, not just "Vercel + Render"

---

## Phase 1: AWS Account Setup ✅ COMPLETED

### What Was Done
1. Created AWS account with free tier enabled
2. Set up billing alerts ($50 limit to catch overages)
3. Created IAM user `github-actions-deployer` with deployment permissions
4. Generated AWS access keys and stored in GitHub Secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION` = `us-east-1`

### Reference
- Full setup guide: `aws/PHASE1-AWS-ACCOUNT-SETUP.md`
- IAM policy: `aws/iam-policy.json`

---

## Phase 2: Containerization (Docker) ✅ COMPLETED

### Architecture
```
Local Development (Docker)
├─ PostgreSQL Database (port 5432)
├─ FastAPI Backend (port 8000)
└─ React + Nginx Frontend (port 3000)
    └─ Proxies /api → Backend:8000
```

### Files Created
| File | Purpose |
|------|---------|
| `backend/Dockerfile` | Build FastAPI container (Python 3.11-slim) |
| `frontend-react/Dockerfile` | Build React with multi-stage Nginx (Node 18 → Nginx Alpine) |
| `frontend-react/nginx.conf` | Nginx config to serve React + proxy API |
| `docker-compose.yml` | Orchestrates all 3 services |
| `.dockerignore` files | Optimize image sizes |
| `.env.example` | Environment template |
| `DOCKER-QUICKSTART.md` | Quick reference for Docker commands |

### Dependencies Cleaned
Removed all development-only packages from `requirements.txt`:
- ❌ Removed: ipython, jupyter, debugpy, streamlit, etc.
- ✅ Kept: fastapi, uvicorn, sqlalchemy, psycopg2, sentence-transformers, nltk, numpy, pandas, scikit-learn

**Python Version Upgrade**: 3.10 → 3.11 (required by modern packages like numpy 2.4.6+)

### Key Design Decisions
1. **Multi-stage Frontend Build**: Reduces final image size from 400MB → 50MB
2. **Environment Variables**: All config via .env (no hardcoding secrets)
3. **Health Checks**: Both backend and database have health checks
4. **Docker Network**: Internal `movie-network` for service-to-service communication

---

## Issues Encountered & Solutions

### Issue 1: YAML Syntax Error in docker-compose.yml
**Error**: `mapping values are not allowed in this context` on line 34  
**Root Cause**: Invalid bash-style error syntax `${VAR:?Error...}` in YAML  
**Fix**: Changed to `${VAR:-default}` syntax

### Issue 2: Python Dependencies Incompatible with 3.10
**Error**: `ipython==9.13.0` requires Python >=3.11  
**Root Cause**: requirements.txt had version conflicts for Python 3.10  
**Fix**: 
- Upgraded base image to Python 3.11-slim
- Updated numpy to 2.2.6 (compatible with 3.11)
- Cleaned out dev-only dependencies

### Issue 3: Missing NLTK in Requirements
**Error**: `ModuleNotFoundError: No module named 'nltk'`  
**Root Cause**: Accidentally removed nltk when cleaning dependencies, but it's used in production code  
**Fix**: Added `nltk==3.9.4` back to requirements.txt

### Issue 4: Database Connection to 127.0.0.1 in Docker
**Error**: `psycopg2.OperationalError: connection to server at "127.0.0.1", port 5432 failed`  
**Root Cause**: 
- `backend/db/database.py` had hardcoded `host="127.0.0.1"`
- Inside Docker, services communicate via service names (e.g., `postgres`), not localhost
- User's DB_PASSWORD had `@` symbol, breaking URL parsing

**Fix**:
- Updated `backend/db/database.py` to read `DATABASE_HOST` from environment (default: `postgres`)
- Made username, password, database name configurable via env vars
- Updated `docker-compose.yml` to pass `DATABASE_HOST: postgres`
- Changed `.env` to use URL-encoded password: `Pranshu123%40` (@ = %40)

### Issue 5: Backend Crashes on Startup - Missing Tables
**Error**: `pandas.errors.DatabaseError: relation "movies" does not exist`  
**Root Cause**: `backend/recommender/engines/content_engine.py` loads movie data at import time before database is seeded  
**Fix**: Wrapped data loading in try-except:
```python
try:
    movies_df = pd.read_sql("SELECT * FROM movies", engine)
    tags_df = pd.read_sql("SELECT * FROM tags", engine)
except Exception as e:
    print(f"Warning: Could not load movies/tags data: {e}")
    movies_df = None
    tags_df = None
```
Also wrapped all data processing in conditional `if movies_df is not None:`

---

## Current Status

### ✅ Complete
- AWS account with free tier and billing alerts
- Docker images built (backend, frontend, postgres)
- docker-compose.yml orchestrates all services
- Environment variables properly configured
- Database connection using Docker service names
- Backend handles missing tables gracefully

### 🔄 In Progress (Next Steps)
1. **Test Docker Locally**: `docker-compose up` should start all services
2. **Seed Database**: Run seed scripts in new terminal
3. **Verify Functionality**: Test endpoints manually
4. **Restart Backend**: After seeding, restart to load data

### ⏭️ Upcoming Phases
- **Phase 3**: GitHub Actions CI/CD pipeline (automated testing + building)
- **Phase 4**: AWS Infrastructure (ECR, RDS, ECS, ALB)
- **Phase 5**: Secrets Management (AWS Secrets Manager)
- **Phase 6**: Local testing before production
- **Phase 7**: Deploy to AWS ECS
- **Phase 8**: Monitoring & CloudWatch (optional)

---

## How to Run (Current State)

### Start Services
```bash
cd e:\D_drive\Personal Dev\Projects\Habitat\Movie-Recommender
docker-compose down  # Clean up any old containers
docker-compose up    # Start backend, frontend, postgres
```

### Seed Database (in new terminal)
```bash
docker exec movie-recommender-backend python scripts/seed_movies.py
docker exec movie-recommender-backend python scripts/seed_ratings.py
docker exec movie-recommender-backend python scripts/seed_tags.py
docker exec movie-recommender-backend python scripts/generate_movie_embeddings.py
```

### Restart Backend (after seeding)
```bash
# Stop (Ctrl+C) then:
docker-compose up
```

### Test
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Key Configuration Files

### .env (LOCAL DEVELOPMENT)
```
DB_USER=postgres
DB_PASSWORD=Pranshu123@
DB_NAME=movie_recommender
DATABASE_HOST=localhost  # Local: localhost, Docker: postgres
SECRET_KEY=StuartBroad604@Wickets
OPENAI_API_KEY=sk-proj-...
```

### docker-compose.yml (PRODUCTION IN DOCKER)
Automatically sets:
- `DATABASE_HOST=postgres` (Docker service name)
- `DATABASE_USER=${DB_USER}`
- `DATABASE_PASSWORD=${DB_PASSWORD}`
- `DATABASE_NAME=${DB_NAME}`

---

## Important Lessons Learned

1. **Docker Networking**: Services in docker-compose communicate by service name, not localhost
2. **URL-Encoded Passwords**: Special characters in connection strings must be URL-encoded (`@` = `%40`)
3. **Import-Time Database Queries**: Bad pattern - causes crashes if DB isn't ready. Wrap in try-except or defer to request time.
4. **Environment Variables**: Make everything configurable to work across local/Docker/AWS
5. **Multi-Stage Docker Builds**: Dramatically reduce image sizes for faster deployment
6. **Free Tier Optimization**: Use python:3.11-slim, nginx:alpine, postgres:15-alpine for minimal resources

---

## Git Commits Made
1. `40796cc` - Phase 2: Add Docker containerization setup
2. `9235182` - Fix docker-compose.yml YAML syntax error on line 34
3. `c17b12f` - Fix Docker build compatibility issues (Python 3.11, dependencies)
4. `1a2f7d4` - Add nltk back to requirements - used in production code
5. `(uncommitted)` - Fix database.py + docker-compose.yml for Docker networking

---

## Next Session Checklist

- [ ] Run `docker-compose up` and verify all services start
- [ ] Run seed scripts and confirm no errors
- [ ] Test frontend at http://localhost:3000
- [ ] Test backend at http://localhost:8000
- [ ] Commit fixes to git if not done
- [ ] Move to Phase 3: GitHub Actions CI/CD

---

## Useful Commands

```bash
# Start everything
docker-compose up

# Stop everything
docker-compose down

# View logs
docker-compose logs -f
docker-compose logs -f backend

# Access backend shell
docker exec -it movie-recommender-backend bash

# Access database
docker exec -it movie-recommender-db psql -U postgres -d movie_recommender

# Rebuild specific service
docker-compose build backend

# Clean everything (WARNING: deletes database)
docker-compose down -v
```

---

## Budget Estimate (AWS Costs)
| Service | Monthly Cost |
|---------|------|
| ECS Fargate (0.5 CPU, 1GB RAM) | $5-10 |
| RDS PostgreSQL (db.t3.micro) | $8-15 |
| ALB | $5-8 |
| CloudWatch/NAT | $0-5 |
| **Total** | **$18-38** |
**Target**: Stay under $30 by maximizing free tier

---

## References
- `aws/PHASE1-AWS-ACCOUNT-SETUP.md` - AWS setup guide
- `aws/PHASE2-DOCKER-SETUP.md` - Comprehensive Docker guide with troubleshooting
- `aws/README.md` - Overview of AWS services
- `DOCKER-QUICKSTART.md` - Quick Docker reference
- `docker-compose.yml` - Full service orchestration config
