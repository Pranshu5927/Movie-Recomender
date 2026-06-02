# Movie Recommender System

A production-style movie recommendation platform built in progressive layers — from popularity-based ranking to collaborative filtering and hybrid ensemble systems, with a roadmap toward semantic AI search and a conversational recommender agent.

## Vision

Inspired by systems used at Netflix, Spotify, YouTube, and Amazon. The project is intentionally built in layers to learn backend engineering, recommender systems, ML systems, vector search, MLOps, and production deployment.

Evolution path:

1. Popularity-based recommendations ✅
2. Content-based filtering ✅
3. Collaborative filtering ✅
4. Hybrid recommendation systems ✅
5. Semantic embeddings + AI conversational recommender _(roadmap)_
6. Fully deployed production architecture _(roadmap)_

---

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL, psycopg2, Pandas, scikit-learn

**Frontend:** React 18 + Vite 5, React Router DOM v6, Axios _(current)_ · Streamlit prototype also in `frontend/`

**ML:** TF-IDF Vectorization, Cosine Similarity, TruncatedSVD, Hybrid Recommendation Systems

**Dataset:** MovieLens `ml-latest-small` — `movies.csv`, `ratings.csv`, `tags.csv`

---

## Project Structure

```text
movie-recommender/
├── backend/
│   ├── api/                    # HTTP routes, auth, query params
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── ratings.py
│   │   ├── watchlist.py
│   │   └── recommendations.py
│   ├── db/
│   ├── models/
│   ├── recommender/            # Recommendation algorithms & ranking
│   │   ├── engines/
│   │   │   └── content_engine.py
│   │   ├── popularity.py
│   │   ├── content_based.py
│   │   ├── personalized_content.py
│   │   ├── collaborative.py
│   │   └── hybrid.py
│   ├── services/
│   │   └── recommendation_service.py
│   └── utils/
├── frontend/                   # Streamlit prototype (Python)
├── frontend-react/             # React app (current)
│   ├── index.html
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── api/
│       │   └── api.js          # Axios API client
│       ├── components/
│       │   ├── HeroBanner.jsx
│       │   ├── MovieCard.jsx
│       │   ├── MovieModal.jsx
│       │   ├── MovieRow.jsx
│       │   ├── Navbar.jsx
│       │   └── ProtectedRoute.jsx
│       ├── context/
│       │   └── AuthContext.jsx
│       ├── pages/
│       │   ├── Auth.jsx
│       │   ├── Home.jsx
│       │   ├── Search.jsx
│       │   └── Watchlist.jsx
│       └── utils/
│           └── movieUtils.js
├── data/
├── notebooks/
├── docker/
├── requirements.txt
└── README.md
```

---

## Architecture

The project separates concerns into four layers, mirroring real production recommendation systems:

| Layer | Folder | Responsibility |
|---|---|---|
| API | `api/` | HTTP routes, authentication, request handling |
| Service | `services/` | Orchestration, homepage assembly, combining recommenders |
| Recommender | `recommender/` | Algorithms, ranking, scoring |
| Engine | `recommender/engines/` | Preprocessing, vectorization, similarity matrices, ML pipelines |

---

## Recommendation Systems

### 1. Popularity-Based — `recommender/popularity.py`
Aggregates MovieLens ratings, scores by average with a minimum rating threshold, and excludes already-rated movies. Surfaces the **Must Watch** row.

### 2. Content-Based Filtering — `recommender/content_based.py`
Pipeline: load movies + tags → clean genres → aggregate tags → build content column → lowercase + stem (NLTK PorterStemmer) → TF-IDF Vectorization → Cosine Similarity. Surfaces the **More Like This** row.

### 3. Personalized Content — `recommender/personalized_content.py`
Analyzes user watch history, fetches similar movies via content engine, aggregates and deduplicates, removes watched movies. Surfaces the **Personalized Content** row.

### 4. Collaborative Filtering — `recommender/collaborative.py`
Builds a user-movie sparse matrix, applies TruncatedSVD (`R ≈ UΣVᵀ`), learns latent embeddings, finds similar users, and recommends highly-rated unseen movies. Surfaces the **Users Also Liked** row.

### 5. Hybrid Recommender — `recommender/hybrid.py`
Ensemble of popularity + content-based + collaborative filtering:

```python
POPULARITY_WEIGHT    = 0.2
CONTENT_WEIGHT       = 0.4
COLLABORATIVE_WEIGHT = 0.4
```

Surfaces the **Personalized For You** row.

---

## API Reference

```text
POST  /auth/signup
POST  /auth/login
GET   /me

GET   /movies
GET   /movies/search

POST  /rate

POST  /watchlist/add
GET   /watchlist
POST  /watchlist/remove

GET   /recommendations
GET   /recommendations/content
```

Authentication uses JWT. Protected routes depend on `get_current_user`. Secret key stored in `.env`.

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

---

## Getting Started

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your `.env` with database credentials and JWT secret key.
4. Download MovieLens `ml-latest-small` and place `movies.csv`, `ratings.csv`, `tags.csv` under `data/`.
5. Run the API:
   ```bash
   uvicorn backend.api.main:app --reload
   ```
6. Run the React frontend:
   ```bash
   cd frontend-react
   npm install
   npm run dev
   ```
   The app will be available at `http://localhost:5173`.

---

## Homepage Layout

Netflix-style homepage assembled by `services/recommendation_service.py`:

```
[ Search Bar ]
--------------------------------------------------
🔥  Must Watch            (popularity-based)
🎭  More Like {movie}     (content-based)
👥  Users Also Liked      (collaborative filtering)
🧠  Personalized For You  (hybrid ensemble)
--------------------------------------------------
```

---

## Roadmap

**Frontend**
- [x] React 18 + Vite frontend (`frontend-react/`)
- [x] Netflix-style homepage with movie rows (HeroBanner, MovieRow, MovieCard)
- [x] Movie detail modal (MovieModal)
- [x] Auth pages, Search page, Watchlist page
- [x] JWT auth via React Context (AuthContext)
- [ ] Next.js migration _(optional — for SSR/SEO)_
- [ ] Hover previews / trailer embeds

**AI & Embeddings**
- [ ] Sentence transformers / OpenAI embeddings
- [ ] Vector database for semantic search
- [ ] Conversational recommender agent ("Movies like Interstellar but darker")

**Service Layer**
- [ ] Trending row
- [ ] Continue Watching
- [ ] Because You Watched

**Deployment**
- [ ] React frontend → Vercel
- [ ] FastAPI backend → Render / Railway
- [ ] PostgreSQL cloud deployment
- [ ] Docker, CI/CD pipelines
