# Phase 2 Quick Start

## TL;DR — Get Docker Running in 5 Minutes

### 1. Copy environment template
```bash
cp .env.example .env
```

### 2. Edit .env and add your OpenAI key
```bash
# In .env, set:
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
```

### 3. Build and start
```bash
docker-compose build
docker-compose up
```

### 4. Open browser
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### 5. Seed database (one-time only)
```bash
# In a new terminal:
docker exec movie-recommender-backend python scripts/seed_movies.py
docker exec movie-recommender-backend python scripts/seed_ratings.py
docker exec movie-recommender-backend python scripts/seed_tags.py
docker exec movie-recommender-backend python scripts/generate_movie_embeddings.py
```

---

## Testing Checklist

- [ ] Backend responds: `curl http://localhost:8000/`
- [ ] Frontend loads: Open http://localhost:3000 in browser
- [ ] Database works: `curl http://localhost:8000/movies`
- [ ] Can sign up: Submit form on frontend
- [ ] No errors in logs: `docker-compose logs`

---

## Troubleshooting

**Port already in use?**
```bash
# Change in docker-compose.yml:
# "3000:80" → "3001:80"
```

**OPENAI_API_KEY not set?**
```bash
# Add to .env:
OPENAI_API_KEY=sk-proj-...
```

**Container won't start?**
```bash
docker-compose logs backend  # See error message
```

---

## More Info

See `aws/PHASE2-DOCKER-SETUP.md` for complete guide with explanations.
