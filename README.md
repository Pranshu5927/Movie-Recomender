# Movie Recommender System

A production-style AI movie recommendation platform built in progressive layers — from popularity-based ranking through collaborative filtering, semantic embeddings, an LLM-powered recommendation engine, and a conversational AI recommender with multi-turn memory.

## Vision

Inspired by systems used at Netflix, Spotify, YouTube, and Amazon. Built iteratively to learn backend engineering, recommender systems, ML systems, vector search, LLM integration, and production deployment.

**Evolution path:**

1. Popularity-based recommendations ✅
2. Content-based filtering ✅
3. Collaborative filtering (SVD) ✅
4. Hybrid recommendation systems ✅
5. Semantic embeddings + semantic search ✅
6. AI recommendation engine (LLM query parsing + re-ranking) ✅
7. Conversational AI recommender (multi-turn chat with memory) ✅
8. Deployment pipeline 🔜

---

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL, psycopg2, Pandas, scikit-learn, OpenAI (gpt-4.1-mini)

**Frontend:** React 18 + Vite 5, React Router DOM v6, Axios

**ML:** TF-IDF Vectorization, Cosine Similarity, TruncatedSVD, sentence-transformers (`all-MiniLM-L6-v2`)

**Dataset:** MovieLens `ml-latest-small` — `movies.csv`, `ratings.csv`, `tags.csv`

---

## Project Structure

```
movie-recommender/
├── backend/
│   ├── main.py                 # FastAPI entry — registers all routers
│   ├── api/
│   │   ├── auth.py             # POST /auth/signup, /auth/login
│   │   ├── users.py            # GET /me
│   │   ├── movies.py           # GET /movies, /movies/search
│   │   ├── ratings.py          # POST /rate
│   │   ├── watchlist.py        # /watchlist/*
│   │   ├── recommendations.py  # GET /recommendations, /recommendations/content
│   │   ├── semantic.py         # GET /search/semantic
│   │   ├── ai.py               # GET /ai/recommend
│   │   └── chat.py             # POST /chat/
│   ├── db/
│   │   └── database.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── rating.py
│   │   ├── watchlist.py
│   │   └── recommendation.py   # Unified Recommendation schema
│   ├── utils/
│   │   └── auth.py             # JWT + get_current_user dependency
│   ├── recommender/
│   │   ├── utils.py            # normalize_scores()
│   │   ├── popularity.py
│   │   ├── content_based.py
│   │   ├── personalized_content.py
│   │   ├── collaborative.py
│   │   ├── hybrid.py
│   │   └── engines/
│   │       └── content_engine.py
│   ├── services/
│   │   ├── recommendation_service.py
│   │   └── semantic_service.py
│   ├── embeddings/
│   │   ├── embedding_service.py
│   │   └── semantic_search.py
│   ├── explainability/
│   │   └── recommendation_explainer.py
│   ├── ai/                     # LLM-powered recommendation engine
│   │   ├── schemas.py
│   │   ├── llm_service.py      # Single OpenAI wrapper
│   │   ├── query_parser.py
│   │   ├── recommendation_pipeline.py
│   │   ├── reranker.py
│   │   └── explanation_generator.py
│   ├── agents/                 # Conversational AI agent
│   │   ├── schemas.py
│   │   ├── prompts.py
│   │   ├── chatbot.py          # Multi-turn intent extraction
│   │   └── recommendation_agent.py
│   └── scripts/
│       ├── seed_movies.py
│       ├── seed_ratings.py
│       ├── seed_tags.py
│       └── generate_movie_embeddings.py
├── frontend-react/
│   └── src/
│       ├── api/api.js
│       ├── context/AuthContext.jsx
│       ├── utils/movieUtils.js
│       ├── components/
│       │   ├── HeroBanner.jsx
│       │   ├── MovieCard.jsx
│       │   ├── MovieModal.jsx
│       │   ├── MovieRow.jsx
│       │   ├── Navbar.jsx
│       │   └── ProtectedRoute.jsx
│       └── pages/
│           ├── Auth.jsx
│           ├── Home.jsx
│           ├── Search.jsx
│           ├── Watchlist.jsx
│           ├── AIRecommend.jsx  # Natural-language AI recommendations
│           └── Chat.jsx         # Multi-turn conversational recommender
├── data/ml-latest-small/
├── requirements.txt
└── context.md                  # Full LLM-readable codebase context
```

---

## Architecture

Four backend layers mirror real production recommendation systems:

| Layer | Folder | Responsibility |
|---|---|---|
| API | `api/` | HTTP routes, auth, request handling |
| Service | `services/` | Orchestration, homepage assembly |
| Recommender | `recommender/` | Algorithms, ranking, scoring |
| Engine | `recommender/engines/` | Preprocessing, vectorization, ML pipelines |

Two AI layers sit on top:

| Layer | Folder | Responsibility |
|---|---|---|
| AI | `ai/` | LLM query parsing, candidate retrieval, re-ranking, explanation |
| Agent | `agents/` | Multi-turn conversation, intent extraction across turns |

---

## Recommendation Systems

### Traditional Recommenders

All recommenders return a **unified schema** with `score`, `normalized_score`, `vote_count`, `reasons`, and `metadata`. Normalization is applied server-side — the frontend never manipulates scores.

| Recommender | File | Algorithm | Homepage Row |
|---|---|---|---|
| Popularity | `popularity.py` | AVG rating, COUNT > 50 | 🔥 Must Watch |
| Content-Based | `content_based.py` | TF-IDF + cosine similarity | 🎭 More Like This |
| Personalized | `personalized_content.py` | User TF-IDF profile vector | 🧠 Personalized |
| Collaborative | `collaborative.py` | TruncatedSVD + user similarity | 👥 Users Also Liked |
| Hybrid | `hybrid.py` | Weighted ensemble (pop 0.2 · content 0.4 · collab 0.4) | 🔄 Hybrid |

### Semantic Search

`scripts/generate_movie_embeddings.py` encodes each movie's title + genres + tags with `all-MiniLM-L6-v2` and stores the 384-dim vectors in PostgreSQL. At query time, `semantic_search.py` encodes the query and does a brute-force cosine similarity scan.

Exposed as `GET /search/semantic` and as a toggle in the Browse page.

### AI Recommendation Engine (`GET /ai/recommend`)

Three sequential LLM calls via `gpt-4.1-mini`:
1. **Query Parser** — extracts genres, moods, themes, similar_to titles from natural language
2. **Candidate Retrieval** — pulls up to 50 candidates from semantic search + content-based + popularity
3. **Re-ranker** — LLM ranks candidates by relevance to the original query
4. **Explanation Generator** — writes a 2–3 sentence explanation of why the films fit

Example:
```
GET /ai/recommend?query=dark sci-fi movies like Interstellar

→ {
    "query": "dark sci-fi movies like Interstellar",
    "explanation": "Arrival and Moon share Interstellar's introspective, cerebral approach...",
    "movies": [...]
  }
```

### Conversational Recommender (`POST /chat/`)

Multi-turn chat where each turn:
1. **Intent Extraction** — LLM sees full conversation history and collapses it into a standalone search query
2. **Recommendation Pipeline** — runs the full AI pipeline on the extracted intent
3. **Explanation** — LLM generates a conversational reply

```
Turn 1: "Recommend mind-bending sci-fi"         → intent: "mind-bending sci-fi"
Turn 2: "Something darker"                       → intent: "dark mind-bending sci-fi"
Turn 3: "Nothing too old"                        → intent: "dark mind-bending sci-fi after 2000"
```

---

## API Reference

```
POST  /auth/signup                           Register new user
POST  /auth/login                            Authenticate, get JWT

GET   /me                          (auth)   Current user info

GET   /movies                               List movies
GET   /movies/search?query=...              Keyword search

POST  /rate                        (auth)   Submit 1–5 star rating

POST  /watchlist/add               (auth)   Add to watchlist
GET   /watchlist                   (auth)   Get watchlist
DELETE /watchlist/{movie_id}       (auth)   Remove from watchlist

GET   /recommendations             (auth)   Netflix-style homepage (4 rows)
GET   /recommendations/content?movie_title= More Like This

GET   /search/semantic?query=...            Semantic search

GET   /ai/recommend?query=...               AI-powered recommendation
POST  /chat/                                Conversational recommender
```

Auth header: `Authorization: Bearer <token>`

---

## Database Schema

| Table | Key Columns |
|---|---|
| `users` | id, username, email, password_hash, created_at |
| `movies` | movie_id, title, genres |
| `ratings` | id, user_id, movie_id, rating, created_at |
| `ml_ratings` | user_id, movie_id, rating, timestamp _(MovieLens data)_ |
| `tags` | user_id, movie_id, tag, timestamp |
| `watchlist` | id, user_id, movie_id, created_at |
| `movie_embeddings` | movie_id, embedding (JSON, 384-dim) |

---

## Frontend Pages

| Route | Page | Description |
|---|---|---|
| `/auth` | Auth | Login / Sign Up |
| `/` | Home | Netflix-style homepage with 4 recommendation rows |
| `/search` | Search | Keyword + semantic search with mode toggle |
| `/watchlist` | Watchlist | User's saved movies |
| `/ai` | AI Picks | Natural-language AI recommendation with explanation |
| `/chat` | Chat | Multi-turn conversational recommender |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL running locally
- OpenAI API key

### Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate        # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
```

Create `backend/.env`:
```
DATABASE_PASSWORD=your_pg_password
SECRET_KEY=your_jwt_secret
OPENAI_API_KEY=sk-proj-...
```

Seed the database:
```bash
python scripts/seed_movies.py
python scripts/seed_ratings.py
python scripts/seed_tags.py
python scripts/generate_movie_embeddings.py  # takes a few minutes
```

Start the API:
```bash
uvicorn main:app --reload
# Runs on http://localhost:8000
```

### Frontend

```bash
cd frontend-react
npm install
npm run dev
# Runs on http://localhost:3000
```

The Vite dev server proxies `/api/*` to `http://localhost:8000`.

---

## Roadmap

**Completed**
- [x] Popularity, content-based, collaborative, hybrid recommenders
- [x] Unified `Recommendation` schema with normalized scores across all sources
- [x] Semantic embeddings (all-MiniLM-L6-v2) stored in PostgreSQL
- [x] Semantic search (keyword + semantic toggle in Browse)
- [x] AI recommendation engine (`GET /ai/recommend`) with LLM query parsing + re-ranking
- [x] Conversational recommender (`POST /chat/`) with multi-turn intent memory
- [x] React frontend: Home, Search, Watchlist, AI Picks, Chat pages

**Next**
- [ ] User preference memory (persistent `user_preferences` table for long-term personalization)
- [ ] Vector database (pgvector / Pinecone) for scalable ANN search
- [ ] Auth on AI/chat endpoints + exclude watched movies from AI results
- [ ] LLM response streaming for faster chat feel
- [ ] CORS configuration for deployment
- [ ] Deployment: React → Vercel, FastAPI → Render/Railway, DB → Neon
