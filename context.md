# Movie Recommender System — Full Codebase Context

> This file is the single source of truth for any LLM building features on top of this codebase.
> It covers every file, what it does, what it returns, and how the pieces connect.

---

## Vision & Goals

A production-style movie recommendation platform inspired by Netflix/Spotify. Built in layers:

1. Popularity-based recommendations ✅
2. Content-based filtering ✅
3. Collaborative filtering ✅
4. Hybrid recommendation system ✅
5. Semantic embeddings + search ✅
6. Conversational AI recommender agent 🚧 (scaffolded, not implemented)
7. Deployment pipeline 🔜

Learning goals: backend engineering, recommender systems, ML systems, vector search, MLOps, full-stack, production deployment.

---

## Tech Stack

### Backend
- **Python** + **FastAPI** (web framework)
- **SQLAlchemy** (DB connection/raw SQL — NOT ORM-style)
- **psycopg2** (direct PostgreSQL driver)
- **Pandas** (data manipulation)
- **scikit-learn** (TF-IDF, TruncatedSVD, cosine_similarity)
- **sentence-transformers** (`all-MiniLM-L6-v2` — semantic embeddings)
- **NLTK** (PorterStemmer for text normalization)
- **python-jose** (JWT encoding/decoding)
- **passlib[bcrypt]** (password hashing)
- **python-dotenv** (env var loading)

### Frontend
- **React 18** + **Vite 5** (SPA build tool)
- **React Router DOM v6** (client-side routing)
- **Axios** (HTTP client with interceptors)

### Database
- **PostgreSQL** (local: `localhost:5432`, db: `movie_recommender`, user: `postgres`)

### Dataset
- **MovieLens ml-latest-small** (`data/ml-latest-small/`)
  - `movies.csv`: movie_id, title, genres
  - `ratings.csv`: userId, movieId, rating, timestamp
  - `tags.csv`: userId, movieId, tag, timestamp

---

## Directory Structure

```
movie-recommender/
├── backend/
│   ├── main.py                          # FastAPI app entry point
│   ├── .env                             # Secrets (DATABASE_PASSWORD, SECRET_KEY, etc.)
│   ├── api/                             # HTTP route handlers
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── movies.py
│   │   ├── ratings.py
│   │   ├── watchlist.py
│   │   ├── recommendations.py
│   │   └── semantic.py
│   ├── db/
│   │   └── database.py                  # SQLAlchemy engine + SessionLocal
│   ├── models/                          # (directory exists, ORM models if added later)
│   ├── schemas/                         # Pydantic request/response models
│   │   ├── auth.py
│   │   ├── rating.py
│   │   └── watchlist.py
│   ├── utils/
│   │   └── auth.py                      # JWT decode + get_current_user dependency
│   ├── recommender/                     # All recommendation algorithms
│   │   ├── popularity.py
│   │   ├── content_based.py
│   │   ├── personalized_content.py
│   │   ├── collaborative.py
│   │   ├── hybrid.py
│   │   └── engines/
│   │       └── content_engine.py        # TF-IDF + cosine similarity pipeline
│   ├── services/                        # Orchestration layer
│   │   ├── recommendation_service.py
│   │   └── semantic_service.py
│   ├── embeddings/                      # Semantic search layer
│   │   ├── embedding_service.py         # SentenceTransformer singleton
│   │   └── semantic_search.py           # Embedding load + cosine search
│   ├── explainability/
│   │   └── recommendation_explainer.py  # Human-readable reason generation
│   ├── agents/                          # 🚧 Conversational AI agent (all files empty)
│   │   ├── chatbot.py
│   │   ├── prompts.py
│   │   ├── recommendation_agent.py
│   │   └── schemas.py
│   └── scripts/                         # One-time data seeding / setup
│       ├── seed_movies.py
│       ├── seed_ratings.py
│       ├── seed_tags.py
│       ├── generate_movie_embeddings.py
│       └── test_db_connection.py
├── frontend-react/                      # React SPA (active frontend)
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── api/
│       │   └── api.js                   # Axios client + all API groups
│       ├── context/
│       │   └── AuthContext.jsx          # Global auth state (user, login, logout)
│       ├── utils/
│       │   └── movieUtils.js            # Genre gradients, title cleaning, score formatting
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
│           └── Watchlist.jsx
├── frontend/                            # Streamlit prototype (kept for reference, not active)
├── data/
│   └── ml-latest-small/
│       ├── movies.csv
│       ├── ratings.csv
│       └── tags.csv
├── notebooks/
├── docker/
├── requirements.txt
└── context.md                           # This file
```

---

## Database Schema

All tables in PostgreSQL database `movie_recommender`:

### `users`
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| username | VARCHAR | |
| email | VARCHAR | unique |
| password_hash | VARCHAR | bcrypt hashed |
| created_at | TIMESTAMP | |

### `movies`
| Column | Type | Notes |
|---|---|---|
| movie_id | INT PK | from MovieLens |
| title | VARCHAR | includes "(YYYY)" at end |
| genres | VARCHAR | pipe-separated, e.g. `Action\|Comedy` |

### `ratings`
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| user_id | INT FK → users | |
| movie_id | INT FK → movies | |
| rating | FLOAT | 1.0–5.0 |
| created_at | TIMESTAMP | |

### `ml_ratings`
| Column | Type | Notes |
|---|---|---|
| user_id | INT | MovieLens user IDs |
| movie_id | INT | |
| rating | FLOAT | |
| timestamp | BIGINT | |

Used for: popularity recommender, collaborative filtering SVD

### `tags`
| Column | Type | Notes |
|---|---|---|
| user_id | INT | |
| movie_id | INT | |
| tag | VARCHAR | free-text MovieLens tag |
| timestamp | BIGINT | |

Used for: content engine feature building

### `watchlist`
| Column | Type | Notes |
|---|---|---|
| id | SERIAL PK | |
| user_id | INT FK → users | |
| movie_id | INT FK → movies | |
| created_at | TIMESTAMP | |

Unique constraint: (user_id, movie_id)

### `movie_embeddings`
| Column | Type | Notes |
|---|---|---|
| movie_id | INT PK | FK → movies |
| embedding | TEXT | JSON-serialized list of 384 floats |

---

## Environment Variables (`backend/.env`)

```
DATABASE_PASSWORD=...         # Used to build local PostgreSQL connection string
SECRET_KEY=...                # JWT signing key
DATABASE_URL=postgresql://... # Neon cloud URL (in .env but NOT used in active code)
OPENAI_API_KEY=sk-proj-...    # Stored but currently unused
```

The active DB connection string is built in `db/database.py` as:
```
postgresql://postgres:{DATABASE_PASSWORD}@127.0.0.1:5432/movie_recommender
```

---

## Backend Files — Complete Reference

---

### `backend/main.py`

**Entry point for the FastAPI application.**

```python
app = FastAPI()

app.include_router(auth_router,            prefix="/auth")
app.include_router(users_router)           # /me
app.include_router(movies_router)          # /movies, /movies/search
app.include_router(ratings_router)         # /rate
app.include_router(watchlist_router)       # /watchlist/*
app.include_router(recommendations_router) # /recommendations/*
app.include_router(semantic_router)        # /search/semantic

@app.get("/")
def home() → {"message": "Movie Recommender API is running"}
```

Run with: `uvicorn main:app --reload` from `backend/`

---

### `backend/db/database.py`

**Database connection factory.**

- Creates SQLAlchemy `engine` for PostgreSQL using `DATABASE_PASSWORD` from env
- Creates `SessionLocal` (not used — code uses `engine.connect()` with raw SQL directly)
- Exports: `engine`, `SessionLocal`
- Used by: almost every backend module that needs DB access

```python
engine = create_engine(f"postgresql://postgres:{pw}@127.0.0.1:5432/movie_recommender")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

---

### `backend/schemas/auth.py`

**Pydantic models for auth requests.**

```python
class UserSignup(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str
```

---

### `backend/schemas/rating.py`

```python
class RatingCreate(BaseModel):
    movie_id: int
    rating: float
```

---

### `backend/schemas/watchlist.py`

```python
class WatchlistCreate(BaseModel):
    movie_id: int
```

---

### `backend/utils/auth.py`

**JWT authentication dependency.**

Constants:
- `SECRET_KEY` — from `.env`
- `ALGORITHM = "HS256"`

```python
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())) → dict
```
- Decodes `Authorization: Bearer <token>` header
- Validates signature and expiration (`exp` claim)
- Fetches matching user row from `users` table
- Returns: `{"id": int, "username": str, "email": str}`
- Raises: `HTTPException(401)` on invalid/expired token or user not found

Used as a FastAPI `Depends()` on all protected endpoints.

---

### `backend/api/auth.py`

**Auth routes.**

```
POST /auth/signup
  Body: UserSignup {username, email, password}
  Logic: hash password with bcrypt, check email uniqueness, INSERT into users
  Returns: {"message": "User created successfully"}
  Raises: 400 if email already exists

POST /auth/login
  Body: UserLogin {email, password}
  Logic: fetch user by email, verify bcrypt hash, create JWT (24h expiry)
  Returns: {"access_token": str, "token_type": "bearer"}
  Raises: 401 if invalid credentials
```

---

### `backend/api/users.py`

```
GET /me
  Auth: Required (Bearer token)
  Returns: {"user": {"id": int, "username": str, "email": str}}
```

---

### `backend/api/movies.py`

```
GET /movies
  Auth: Not required
  Returns: [{movie_id, title, genres}, ...]  (first 20 rows)

GET /movies/search?query=<str>
  Auth: Not required
  Logic: SELECT ... WHERE title ILIKE '%query%' LIMIT 20
  Returns: [{movie_id, title, genres}, ...]
```

---

### `backend/api/ratings.py`

```
POST /rate
  Auth: Required
  Body: RatingCreate {movie_id: int, rating: float}
  Logic: INSERT into ratings table
  Returns: {"message": "Rating added successfully"}
```

---

### `backend/api/watchlist.py`

```
POST /watchlist/add
  Auth: Required
  Body: WatchlistCreate {movie_id: int}
  Logic: INSERT into watchlist, skip if already exists
  Returns: {"message": "Added to watchlist"}

GET /watchlist
  Auth: Required
  Logic: SELECT w.movie_id, m.title, m.genres FROM watchlist JOIN movies
  Returns: [{movie_id, title, genres}, ...]

DELETE /watchlist/{movie_id}
  Auth: Required
  Logic: DELETE FROM watchlist WHERE user_id=? AND movie_id=?
  Returns: {"message": "Removed from watchlist"}
```

---

### `backend/api/recommendations.py`

```
GET /recommendations
  Auth: Required
  Calls: services/recommendation_service.get_homepage_recommendations(user_id)
  Returns: {
    "must_watch":       {"title": "🔥 Must Watch",          "movies": [...]},
    "personalized":     {"title": "🧠 Personalized For You", "movies": [...]},
    "users_also_liked": {"title": "👥 Users Also Liked",     "movies": [...]},
    "hybrid":           {"title": "🔄 Hybrid Recommendations","movies": [...]}
  }

GET /recommendations/content?movie_title=<str>
  Auth: Not required
  Calls: services/recommendation_service.get_content_based_recommendations(movie_title)
  Returns: {"title": "🎭 More Like {movie_title}", "movies": [...]}
```

---

### `backend/api/semantic.py`

```
GET /search/semantic?query=<str>&limit=10
  Auth: Not required
  Calls: services/semantic_service.SemanticService.search(query, limit)
  Returns: {"query": str, "results": [{movie_id, title, score}, ...]}
```

---

### `backend/services/recommendation_service.py`

**Orchestration layer — assembles the homepage.**

```python
def get_homepage_recommendations(user_id: int) → dict
```
Calls all four recommenders sequentially and assembles sections:
1. `popularity.get_popular_recommendations(user_id)` → `must_watch`
2. `hybrid.get_hybrid_recommendations(user_id)` → `personalized`
3. `collaborative.get_collaborative_recommendations(user_id)` → `users_also_liked`
4. `hybrid.get_hybrid_recommendations(user_id)` → `hybrid`
   - Normalizes `hybrid_score` field to 0–1 range (divides by max hybrid_score)

```python
def get_content_based_recommendations(movie_title: str) → dict
```
Calls `content_based.get_similar_movies(movie_title)` and wraps result.

---

### `backend/services/semantic_service.py`

```python
class SemanticService:
    @staticmethod
    def search(query: str, limit: int = 10) → List[dict]
```
Thin wrapper over `embeddings.semantic_search.semantic_search(query, limit)`.

---

### `backend/recommender/popularity.py`

**Popularity-based recommender.**

```python
def get_popular_recommendations(user_id: int) → List[dict]
```

Algorithm:
1. Query `ml_ratings` joined with `movies`
2. Exclude movies already rated by `user_id` (from `ratings` table)
3. Group by movie, compute AVG(rating) and COUNT(rating)
4. Filter: COUNT > 50 (minimum vote threshold)
5. ORDER BY avg_rating DESC, LIMIT 20

Returns list of:
```python
{
    "movie_id": int,
    "title": str,
    "genres": str,
    "score": float,         # avg_rating from ml_ratings
    "vote_count": int,
    "recommendation_source": "popularity"
}
```

Used for: `🔥 Must Watch` row

---

### `backend/recommender/content_based.py`

**Content-based "More Like This" recommender.**

Imports at module level from `engines/content_engine.py`:
- `movies_df` — processed DataFrame
- `similarity` — cosine similarity matrix

```python
def get_similar_movies(movie_title: str) → List[dict]
```

Algorithm:
1. Find `movie_title` in `movies_df` index
2. Get row of similarity scores from the matrix
3. Sort descending, exclude self (score = 1.0)
4. Return top 5

Returns list of:
```python
{
    "movie_id": int,
    "title": str,
    "genres": str,
    "score": float,         # cosine similarity (0–1)
    "recommendation_source": "content_based"
}
```

Used for: `🎭 More Like {title}` in MovieModal

---

### `backend/recommender/personalized_content.py`

**User-profile content recommender.**

Imports `movies_df` and `vectors` (TF-IDF vectors) from `content_engine.py`.

```python
def get_personalized_recommendations(user_id: int, top_n: int = 20) → List[dict]
```

Algorithm:
1. Fetch user's rated movies with `rating >= 4` from `ratings` table
2. Cold start check: return `[]` if no qualifying ratings
3. Get TF-IDF vectors for liked movies from `vectors`
4. Build user profile = `np.mean(liked_vectors, axis=0)` (centroid)
5. Compute cosine similarity between profile and all movie vectors
6. Filter out already-rated movies
7. Sort descending, return top `top_n`

Returns list of:
```python
{
    "movie_id": int,
    "title": str,
    "genres": str,
    "score": float,         # cosine similarity (0–1)
    "recommendation_source": "personalized_content"
}
```

Used for: `🧠 Personalized For You` row (currently via hybrid layer)

---

### `backend/recommender/collaborative.py`

**Collaborative filtering via SVD matrix factorization.**

**Module-level preprocessing (runs on import, ~seconds):**
1. Load all `ml_ratings` and `movies` from PostgreSQL
2. Build user-movie rating matrix (rows=users, cols=movies, values=rating, fillna=0)
3. Convert to scipy CSR sparse matrix
4. Apply `TruncatedSVD(n_components=50)` → latent user embeddings (`U`)
5. Compute cosine similarity matrix between all users in latent space

```python
def get_collaborative_recommendations(user_id: int, top_n: int = 20) → List[dict]
```

Algorithm:
1. Find user's row index in the user-movie matrix
2. If user not found in matrix → return `[]`
3. Get top 10 most similar users (exclude self)
4. For each similar user: collect movies they rated >= 4
5. Exclude movies already rated by target user
6. Aggregate score = sum of similarity_score per movie across similar users
7. Sort by aggregated score DESC, return top `top_n`

Returns list of:
```python
{
    "movie_id": int,
    "title": str,
    "genres": str,
    "score": float,         # aggregated similarity score
    "recommendation_source": "collaborative"
}
```

Used for: `👥 Users Also Liked` row

---

### `backend/recommender/hybrid.py`

**Ensemble recommender combining all three algorithms.**

Weights:
```python
POPULARITY_WEIGHT    = 0.2
CONTENT_WEIGHT       = 0.4
COLLABORATIVE_WEIGHT = 0.4
```

```python
def get_hybrid_recommendations(user_id: int, top_n: int = 20) → List[dict]
```

Algorithm:
1. Get recommendations from:
   - `popularity.get_popular_recommendations(user_id)`
   - `personalized_content.get_personalized_recommendations(user_id)`
   - `collaborative.get_collaborative_recommendations(user_id)`
2. Rank each list by position (rank 1 = best)
3. weighted_score = `(1/rank) * WEIGHT` for each source
4. Aggregate by movie_id: sum weighted scores across sources
5. Sort by `hybrid_score` DESC
6. For each top movie, generate explanations via `RecommendationExplainer.generate(movie)`

Returns list of:
```python
{
    "movie_id": int,
    "title": str,
    "genres": str,
    "score": float,
    "hybrid_score": float,
    "popularity_score": float,
    "content_score": float,
    "collaborative_score": float,
    "recommendation_source": "hybrid",
    "reasons": List[str]    # human-readable, max 2 reasons
}
```

Used for: `🔄 Hybrid Recommendations` row

---

### `backend/recommender/engines/content_engine.py`

**ML preprocessing pipeline for content-based filtering. Runs on import.**

Steps:
1. Load `movies` table and `tags` table from PostgreSQL
2. Clean `genres`: replace `|` with space, remove `"(no genres listed)"`
3. Aggregate `tags` per movie: group by `movie_id`, join all tags with space
4. Merge movies + tags DataFrames on `movie_id`
5. Build `content` column: `genres_clean + " " + aggregated_tags`
6. Lowercase entire content column
7. Apply `PorterStemmer` to every word in content
8. TF-IDF Vectorization: `max_features=5000`, `stop_words='english'`
9. Compute cosine similarity matrix over all movie vectors

Exports (used by other modules):
```python
movies_df   # pd.DataFrame with columns: movie_id, title, genres, content
vectors     # np.ndarray — TF-IDF feature matrix (n_movies × 5000)
similarity  # np.ndarray — cosine similarity matrix (n_movies × n_movies)
```

Imported by: `content_based.py`, `personalized_content.py`

---

### `backend/embeddings/embedding_service.py`

**SentenceTransformer singleton.**

```python
class EmbeddingService:
    _model = None

    @classmethod
    def get_model() → SentenceTransformer
        # Lazy-loads all-MiniLM-L6-v2 on first call

    @classmethod
    def embed_text(text: str) → List[float]
        # Returns 384-dimensional vector
```

---

### `backend/embeddings/semantic_search.py`

**Semantic search implementation.**

```python
def load_movie_embeddings() → pd.DataFrame
```
- Query: `SELECT m.movie_id, m.title, me.embedding FROM movies m JOIN movie_embeddings me ON m.movie_id = me.movie_id`
- Parses JSON string embeddings → Python lists
- Returns DataFrame with columns: `[movie_id, title, embedding]`

```python
def semantic_search(query: str, top_k: int = 10) → List[dict]
```
1. Encode query via `EmbeddingService.embed_text(query)` → 384-dim vector
2. Load all movie embeddings from DB
3. For each movie: compute cosine similarity between query vector and movie vector
4. Sort by similarity DESC
5. Return top `top_k`

Returns list of:
```python
{
    "movie_id": int,
    "title": str,
    "score": float      # cosine similarity (0–1)
}
```

Note: This is a brute-force scan over all embeddings. No ANN index yet.

---

### `backend/explainability/recommendation_explainer.py`

**Generates human-readable recommendation reasons.**

```python
class RecommendationExplainer:
    @staticmethod
    def generate(movie: dict) → List[str]
```

- Reads `content_score`, `collaborative_score`, `popularity_score` from movie dict
- Sorts sources by score DESC
- Takes top 2 sources with score > 0
- Maps to strings:
  - `content` → `"Similar to movies you've enjoyed"`
  - `collaborative` → `"Liked by users with similar tastes"`
  - `popularity` → `"Highly rated by the community"`

Called by: `hybrid.py` after building hybrid scores

---

### `backend/scripts/seed_movies.py`

One-time script. Reads `data/ml-latest-small/movies.csv`, renames `movieId → movie_id`, inserts into `movies` table.

### `backend/scripts/seed_ratings.py`

One-time script. Reads `data/ml-latest-small/ratings.csv`, renames columns, inserts into `ml_ratings` table.

### `backend/scripts/seed_tags.py`

One-time script. Reads `data/ml-latest-small/tags.csv`, inserts into `tags` table.

### `backend/scripts/generate_movie_embeddings.py`

One-time script. For each movie:
- Builds content string: `f"{title}\n{genres}\n{tags}"`
- Encodes with `SentenceTransformer("all-MiniLM-L6-v2")` → 384-dim vector
- Upserts into `movie_embeddings` table (ON CONFLICT DO UPDATE)

### `backend/scripts/test_db_connection.py`

Sanity check script. Connects with psycopg2, runs `SELECT 1`.

---

### `backend/agents/` (🚧 All files empty — planned feature)

| File | Planned Purpose |
|---|---|
| `chatbot.py` | Conversational chat interface handler |
| `recommendation_agent.py` | Agent that calls recommenders and formats chat responses |
| `prompts.py` | System prompts / few-shot examples for the LLM |
| `schemas.py` | Pydantic models for agent request/response |

Conversational recommender examples to support:
- "Recommend mind-bending sci-fi movies"
- "Movies like Interstellar but darker"
- "Funny movies for family night"

The `OPENAI_API_KEY` in `.env` is already present for this use.

---

## API Endpoints — Complete Reference

| Method | Endpoint | Auth | Request | Response |
|---|---|---|---|---|
| POST | `/auth/signup` | No | `{username, email, password}` | `{message}` |
| POST | `/auth/login` | No | `{email, password}` | `{access_token, token_type}` |
| GET | `/me` | Yes | — | `{user: {id, username, email}}` |
| GET | `/movies` | No | — | `[{movie_id, title, genres}]` |
| GET | `/movies/search?query=` | No | query param | `[{movie_id, title, genres}]` |
| POST | `/rate` | Yes | `{movie_id, rating}` | `{message}` |
| POST | `/watchlist/add` | Yes | `{movie_id}` | `{message}` |
| GET | `/watchlist` | Yes | — | `[{movie_id, title, genres}]` |
| DELETE | `/watchlist/{movie_id}` | Yes | path param | `{message}` |
| GET | `/recommendations` | Yes | — | `{must_watch, personalized, users_also_liked, hybrid}` |
| GET | `/recommendations/content?movie_title=` | No | query param | `{title, movies}` |
| GET | `/search/semantic?query=&limit=` | No | query params | `{query, results}` |
| GET | `/` | No | — | `{message}` |

Auth header format: `Authorization: Bearer <jwt_token>`

---

## Frontend Files — Complete Reference

---

### `frontend-react/vite.config.js`

- Dev server: port `3000`
- Proxy: `/api/*` → `http://127.0.0.1:8000` (strips `/api` prefix)
- Plugin: `@vitejs/plugin-react` (Fast Refresh)

---

### `frontend-react/src/api/api.js`

**Central Axios client. All backend calls go through here.**

Axios instance:
- `baseURL: '/api'`
- Request interceptor: adds `Authorization: Bearer <token>` from `localStorage.getItem('token')`
- Response interceptor: on 401 → clears token, redirects to `/auth`

Exported API groups:

```js
authAPI = {
    signup(username, email, password)  → POST /auth/signup
    login(email, password)             → POST /auth/login
}

moviesAPI = {
    getAll()                           → GET /movies
    search(q)                          → GET /movies/search?query=q
}

recommendationsAPI = {
    getHomepage()                      → GET /recommendations
    getContentBased(title)             → GET /recommendations/content?movie_title=title
}

semanticAPI = {
    search(query, limit=10)            → GET /search/semantic?query=query&limit=limit
}

ratingsAPI = {
    rate(movieId, rating)              → POST /rate
}

watchlistAPI = {
    get()                              → GET /watchlist
    add(movieId)                       → POST /watchlist/add
    remove(movieId)                    → DELETE /watchlist/movieId
}

usersAPI = {
    getMe()                            → GET /me
}
```

---

### `frontend-react/src/context/AuthContext.jsx`

**Global auth state. Wraps entire app.**

State:
- `user` — `null` or `{id, username, email}`
- `loading` — `true` while verifying stored token on mount

Methods:
```js
login(email, password)                 → calls authAPI.login(), stores token, fetches /me, sets user
signup(username, email, password)      → calls authAPI.signup(), then login()
logout()                               → removes token from localStorage, sets user to null
```

Hook: `useAuth()` — access `{user, loading, login, signup, logout}` from any component

---

### `frontend-react/src/utils/movieUtils.js`

Utility functions for display:

```js
getGenreGradient(genres: str) → str (CSS gradient)
// Maps first matching genre to a gradient. 16 genres mapped.
// e.g., Action → dark red gradient, Comedy → green gradient

getCleanTitle(title: str) → str
// Removes "(YYYY)" year suffix
// Reorders articles: "Matrix, The" → "The Matrix"

getYear(title: str) → str
// Extracts "(YYYY)" → "YYYY" or "" if not found

getGenres(genres: str) → string[]
// Splits pipe-separated genres string into array

formatScore(movie: obj) → str
// If recommendation_source === "popularity": returns "★ X.X"
// Otherwise: returns "XX% Match" (score * 100, rounded)
```

---

### `frontend-react/src/components/HeroBanner.jsx`

Props: `{ movie, onMoreInfo }`

Renders hero section at top of homepage:
- Background: genre-based CSS gradient via `getGenreGradient()`
- Shows: clean title, year, top 3 genres, `★ avg_rating (vote_count votes)`
- Buttons: "▶ Play" (no-op), "ⓘ More Info" → calls `onMoreInfo(movie)`

---

### `frontend-react/src/components/MovieRow.jsx`

Props: `{ title, movies, onMovieClick }`

Horizontal scrolling movie carousel:
- Left/right arrow buttons (show/hide based on scroll position)
- Each click scrolls 680px
- Renders `<MovieCard>` for each movie
- Ref-based scroll tracking

---

### `frontend-react/src/components/MovieCard.jsx`

Props: `{ movie, onClick }`

Default state:
- Genre-gradient background
- Score badge (top-right) via `formatScore()`
- Title (clean), year, genre tags

Hover overlay:
- Play icon, title, genres
- `reasons` array (max 2) — shown as bullet points
- Keyboard accessible (Enter key triggers onClick)

---

### `frontend-react/src/components/MovieModal.jsx`

Props: `{ movie, onClose, onMovieClick }`

Full-screen modal for movie detail:

On mount:
- `watchlistAPI.get()` → checks if movie is in watchlist
- `recommendationsAPI.getContentBased(movie.title)` → loads "More Like This" section

User actions:
- Add/remove watchlist: `watchlistAPI.add()` / `watchlistAPI.remove()`
- Star rating (1–5): `ratingsAPI.rate()` on click
- Click "More Like This" card → calls `onMovieClick(movie)` (opens new modal)

Feedback: Toast notifications for watchlist/rating actions
Close: X button or Escape key

---

### `frontend-react/src/components/Navbar.jsx`

Features:
- Logo: "FILMIX"
- Nav links: Home (`/`), My List (`/watchlist`), Browse (`/search`)
- Collapsible search bar: opens on icon click, navigates to `/search?q=...` on submit
- User avatar with initials, dropdown: username, email, Logout button
- Scroll detection: applies CSS class when `window.scrollY > 50`

Uses: `useAuth()`, `useNavigate()`, `useLocation()`

---

### `frontend-react/src/components/ProtectedRoute.jsx`

Wrapper for authenticated routes:
- Shows spinner while `loading === true` (initial auth check)
- Redirects to `/auth` if `user === null`
- Renders `children` if authenticated

---

### `frontend-react/src/pages/Auth.jsx`

Login / Sign Up page at `/auth`.

State: `mode` (login|signup), form fields, error, loading

- Toggles between login and signup
- On signup: validates username is present
- On success: redirects to `/` via `useNavigate()`
- Shows backend error messages inline

---

### `frontend-react/src/pages/Home.jsx`

Netflix-style homepage at `/`.

On mount:
1. `recommendationsAPI.getHomepage()` → `sections` state
2. Normalizes `hybrid_score` in hybrid section (divides by max)

Renders:
- `<HeroBanner>` with first movie from `must_watch`
- Four `<MovieRow>` sections: must_watch, personalized, users_also_liked, hybrid
- `<MovieModal>` when card clicked

Error state: message + retry button
Loading state: spinner

---

### `frontend-react/src/pages/Search.jsx`

Search page at `/search`.

State: `query`, `results`, `loading`, `searchMode` (keyword|semantic), `selectedMovie`

- Query synced to URL param `?q=`
- Debounced search (380ms) on input change
- Mode toggle: Keyword (LIKE) vs Semantic (embeddings)
  - Keyword: `moviesAPI.search(query)`
  - Semantic: `semanticAPI.search(query, limit=10)`
- Results displayed as grid of `<MovieCard>`
- Click opens `<MovieModal>`
- Shows result count or "No results" message

---

### `frontend-react/src/pages/Watchlist.jsx`

Watchlist page at `/watchlist`.

On mount: `watchlistAPI.get()`
On modal close: re-fetches watchlist (user may have removed from modal)

Renders:
- Title count: "N titles"
- Grid of `<MovieCard>` components
- Empty state with CTA to browse
- `<MovieModal>` on card click

---

## Call Graph / Dependency Map

```
Browser
 └── React App (frontend-react/src/)
      ├── AuthContext (wraps all routes)
      │    └── authAPI → POST /auth/login, /auth/signup
      │
      ├── ProtectedRoute (guards /, /watchlist)
      │    └── useAuth()
      │
      ├── Navbar
      │    ├── useAuth() → logout()
      │    └── moviesAPI.search() → GET /movies/search
      │
      ├── Home (/)
      │    ├── recommendationsAPI.getHomepage() → GET /recommendations
      │    │    └── FastAPI: api/recommendations.py
      │    │         └── services/recommendation_service.py
      │    │              ├── recommender/popularity.py
      │    │              │    └── SQL: ml_ratings + movies
      │    │              ├── recommender/hybrid.py
      │    │              │    ├── recommender/personalized_content.py
      │    │              │    │    └── engines/content_engine.py (TF-IDF)
      │    │              │    │         └── SQL: movies + tags
      │    │              │    ├── recommender/collaborative.py (SVD)
      │    │              │    │    └── SQL: ml_ratings + movies
      │    │              │    └── explainability/recommendation_explainer.py
      │    │              └── recommender/collaborative.py
      │    └── MovieModal (on click)
      │         ├── recommendationsAPI.getContentBased() → GET /recommendations/content
      │         │    └── recommender/content_based.py
      │         │         └── engines/content_engine.py (cosine similarity matrix)
      │         ├── ratingsAPI.rate() → POST /rate
      │         └── watchlistAPI.add/remove/get() → /watchlist/*
      │
      ├── Search (/search)
      │    ├── moviesAPI.search() → GET /movies/search  (keyword mode)
      │    └── semanticAPI.search() → GET /search/semantic  (semantic mode)
      │         └── FastAPI: api/semantic.py
      │              └── services/semantic_service.py
      │                   └── embeddings/semantic_search.py
      │                        ├── embeddings/embedding_service.py (SentenceTransformer)
      │                        └── SQL: movie_embeddings JOIN movies
      │
      └── Watchlist (/watchlist)
           └── watchlistAPI.get() → GET /watchlist
                └── SQL: watchlist JOIN movies
```

---

## Recommendation Algorithm Reference

| Algorithm | File | Input | Data Source | Output |
|---|---|---|---|---|
| Popularity | `popularity.py` | user_id | `ml_ratings` | Top-rated movies (vote_count > 50) |
| Content-Based | `content_based.py` | movie_title | `movies` + `tags` (via content_engine) | Top 5 similar movies |
| Personalized Content | `personalized_content.py` | user_id | `ratings` + content_engine | User-profile-matched movies |
| Collaborative SVD | `collaborative.py` | user_id | `ml_ratings` | Movies liked by similar users |
| Hybrid | `hybrid.py` | user_id | All three above | Weighted ensemble, top 20 |
| Semantic | `semantic_search.py` | query string | `movie_embeddings` | Cosine similarity to query |

### Hyperparameters

| Parameter | Value | Location |
|---|---|---|
| TF-IDF max_features | 5000 | `content_engine.py` |
| SVD components | 50 | `collaborative.py` |
| Min vote threshold (popularity) | 50 | `popularity.py` |
| Content top-N | 5 | `content_based.py` |
| Collaborative top similar users | 10 | `collaborative.py` |
| Min rating for "liked" | 4.0 | `collaborative.py`, `personalized_content.py` |
| Hybrid: popularity weight | 0.2 | `hybrid.py` |
| Hybrid: content weight | 0.4 | `hybrid.py` |
| Hybrid: collaborative weight | 0.4 | `hybrid.py` |
| Semantic embedding dim | 384 | `all-MiniLM-L6-v2` |
| Semantic default top-K | 10 | `semantic_service.py` |

---

## Movie Object Shapes

### From popularity recommender
```json
{
  "movie_id": 1,
  "title": "Toy Story (1995)",
  "genres": "Adventure|Animation|Children|Comedy|Fantasy",
  "score": 4.2,
  "vote_count": 341,
  "recommendation_source": "popularity"
}
```

### From content-based / semantic recommender
```json
{
  "movie_id": 1,
  "title": "Toy Story (1995)",
  "genres": "Adventure|Animation|Children|Comedy|Fantasy",
  "score": 0.87,
  "recommendation_source": "content_based"
}
```

### From hybrid recommender
```json
{
  "movie_id": 1,
  "title": "Toy Story (1995)",
  "genres": "Adventure|Animation|Children|Comedy|Fantasy",
  "score": 0.72,
  "hybrid_score": 0.531,
  "popularity_score": 0.12,
  "content_score": 0.34,
  "collaborative_score": 0.071,
  "recommendation_source": "hybrid",
  "reasons": ["Similar to movies you've enjoyed", "Liked by users with similar tastes"]
}
```

### Homepage response shape
```json
{
  "must_watch":       { "title": "🔥 Must Watch",           "movies": [...] },
  "personalized":     { "title": "🧠 Personalized For You", "movies": [...] },
  "users_also_liked": { "title": "👥 Users Also Liked",     "movies": [...] },
  "hybrid":           { "title": "🔄 Hybrid Recommendations","movies": [...] }
}
```

---

## Frontend Routing

| Route | Component | Protected |
|---|---|---|
| `/auth` | `Auth.jsx` | No |
| `/` | `Home.jsx` | Yes |
| `/search` | `Search.jsx` | Yes |
| `/watchlist` | `Watchlist.jsx` | Yes |

JWT token stored in `localStorage` under key `'token'`.

---

## Known Gaps / Next Steps

1. **Conversational agent** — `backend/agents/` files are all empty. Planned to use OpenAI API (key already in `.env`). Add route in `api/` (e.g., `POST /chat`), implement agent in `agents/recommendation_agent.py`.

2. **Vector DB** — semantic search currently does brute-force cosine scan over all embeddings. Should migrate to `pgvector` extension or Pinecone for ANN search at scale.

3. **Cold start** — new users get empty personalized/collaborative rows. Consider falling back to popularity for cold-start users.

4. **CORS** — not yet configured in `main.py`. Required before frontend and backend are deployed on different origins.

5. **Deployment** — Planned: React on Vercel, FastAPI on Render/Railway, cloud PostgreSQL (Neon URL already in `.env`).

6. **module-level preprocessing** — `content_engine.py` and `collaborative.py` run heavy ML pipelines on import. This means the first API request triggers slow load. Consider background startup tasks or caching.
