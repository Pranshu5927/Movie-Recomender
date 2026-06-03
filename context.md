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
6. AI recommendation engine (LLM query parsing + re-ranking) ✅
7. Conversational AI recommender (multi-turn chat with memory) ✅
8. Deployment pipeline 🔜

Learning goals: backend engineering, recommender systems, ML systems, vector search, LLM integration, full-stack, production deployment.

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
- **openai** (GPT-4.1-mini — query parsing, re-ranking, explanation generation)
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
│   ├── main.py                              # FastAPI app entry point — registers all routers
│   ├── .env                                 # Secrets (DATABASE_PASSWORD, SECRET_KEY, OPENAI_API_KEY)
│   ├── api/                                 # HTTP route handlers
│   │   ├── auth.py                          # POST /auth/signup, /auth/login
│   │   ├── users.py                         # GET /me
│   │   ├── movies.py                        # GET /movies, /movies/search
│   │   ├── ratings.py                       # POST /rate
│   │   ├── watchlist.py                     # POST/GET/DELETE /watchlist/*
│   │   ├── recommendations.py               # GET /recommendations, /recommendations/content
│   │   ├── semantic.py                      # GET /search/semantic
│   │   ├── ai.py                            # GET /ai/recommend
│   │   └── chat.py                          # POST /chat/
│   ├── db/
│   │   └── database.py                      # SQLAlchemy engine + SessionLocal + DATABASE_URL
│   ├── models/                              # (reserved for ORM models)
│   ├── schemas/                             # Pydantic request/response models
│   │   ├── auth.py                          # UserSignup, UserLogin
│   │   ├── rating.py                        # RatingCreate
│   │   ├── watchlist.py                     # WatchlistCreate
│   │   └── recommendation.py               # Recommendation (unified movie object schema)
│   ├── utils/
│   │   └── auth.py                          # JWT decode + get_current_user dependency
│   ├── recommender/                         # All recommendation algorithms
│   │   ├── popularity.py
│   │   ├── content_based.py
│   │   ├── personalized_content.py
│   │   ├── collaborative.py
│   │   ├── hybrid.py
│   │   ├── utils.py                         # normalize_scores() shared helper
│   │   └── engines/
│   │       └── content_engine.py            # TF-IDF + cosine similarity pipeline (runs on import)
│   ├── services/                            # Orchestration layer
│   │   ├── recommendation_service.py        # Homepage assembly
│   │   └── semantic_service.py              # Thin wrapper over semantic_search
│   ├── embeddings/                          # Semantic search layer
│   │   ├── embedding_service.py             # SentenceTransformer singleton
│   │   └── semantic_search.py               # Embedding load + brute-force cosine search
│   ├── explainability/
│   │   └── recommendation_explainer.py      # Rule-based human-readable reason generation
│   ├── ai/                                  # LLM-powered AI recommendation layer
│   │   ├── schemas.py                       # ParsedMovieQuery, AIRecommendationResponse
│   │   ├── llm_service.py                   # Single OpenAI wrapper (gpt-4.1-mini)
│   │   ├── query_parser.py                  # LLM: raw query → ParsedMovieQuery
│   │   ├── recommendation_pipeline.py       # retrieve_candidates() + run_recommendation_pipeline()
│   │   ├── reranker.py                      # LLM: reorder candidates by relevance
│   │   └── explanation_generator.py         # LLM: write 2-3 sentence explanation
│   ├── agents/                              # Conversational AI agent layer
│   │   ├── schemas.py                       # ChatMessage, ChatRequest, ChatResponse
│   │   ├── prompts.py                       # SYSTEM_PROMPT, INTENT_EXTRACTION_PROMPT
│   │   ├── chatbot.py                       # understand_user_intent() — collapses history to query
│   │   └── recommendation_agent.py          # handle_chat() — orchestrates full chat turn
│   └── scripts/                             # One-time data seeding / setup
│       ├── seed_movies.py
│       ├── seed_ratings.py
│       ├── seed_tags.py
│       ├── generate_movie_embeddings.py
│       └── test_db_connection.py
├── frontend-react/                          # React SPA (active frontend)
│   ├── vite.config.js                       # Port 3000, proxy /api → :8000
│   ├── package.json
│   └── src/
│       ├── api/
│       │   └── api.js                       # Axios client + all API groups
│       ├── context/
│       │   └── AuthContext.jsx              # Global auth state (user, login, logout)
│       ├── utils/
│       │   └── movieUtils.js                # Genre gradients, title cleaning, score formatting
│       ├── components/
│       │   ├── HeroBanner.jsx
│       │   ├── MovieCard.jsx
│       │   ├── MovieModal.jsx
│       │   ├── MovieRow.jsx
│       │   ├── Navbar.jsx                   # Links: Home, My List, Browse, AI Picks, Chat
│       │   └── ProtectedRoute.jsx
│       └── pages/
│           ├── Auth.jsx                     # /auth
│           ├── Home.jsx                     # /
│           ├── Search.jsx                   # /search (keyword + semantic toggle)
│           ├── Watchlist.jsx                # /watchlist
│           ├── AIRecommend.jsx              # /ai (natural-language AI recommendations)
│           └── Chat.jsx                     # /chat (multi-turn conversational recommender)
├── frontend/                                # Streamlit prototype (kept for reference, not active)
├── data/
│   └── ml-latest-small/
├── notebooks/
├── docker/
├── requirements.txt
└── context.md                               # This file
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
| genres | VARCHAR | pipe-separated e.g. `Action\|Comedy` |

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
OPENAI_API_KEY=sk-proj-...    # Used by ai/llm_service.py (gpt-4.1-mini)
```

Active DB connection string built in `db/database.py`:
```
postgresql://postgres:{DATABASE_PASSWORD}@127.0.0.1:5432/movie_recommender
```

---

## Unified Movie Object Schema

All recommenders return the same shape. This is the canonical `Recommendation` object (defined in `schemas/recommendation.py`):

```python
class Recommendation(BaseModel):
    movie_id: int
    title: str
    genres: str
    score: float           # raw score (avg_rating for popularity; cosine sim for others; hybrid_score for hybrid)
    normalized_score: float  # score normalized to 0–1 within its result set (added by normalize_scores())
    recommendation_source: str   # "popularity" | "content_based" | "personalized_content" | "collaborative" | "hybrid"
    vote_count: Optional[int]    # only set for popularity; None for all others
    reasons: List[str]           # human-readable reasons (max 2)
    metadata: Dict[str, Any]     # source-specific extras (avg_rating for popularity; sub-scores for hybrid)
```

### Concrete shapes per source

**Popularity:**
```json
{
  "movie_id": 1, "title": "Toy Story (1995)", "genres": "Adventure|Animation|...",
  "score": 4.21, "normalized_score": 0.95,
  "recommendation_source": "popularity",
  "vote_count": 341,
  "reasons": ["Highly rated by the community"],
  "metadata": {"avg_rating": 4.21}
}
```

**Content-based / Personalized / Collaborative:**
```json
{
  "movie_id": 1, "title": "Arrival (2016)", "genres": "Drama|Sci-Fi",
  "score": 0.874, "normalized_score": 0.91,
  "recommendation_source": "content_based",
  "vote_count": null,
  "reasons": ["Similar content and themes"],
  "metadata": {}
}
```

**Hybrid:**
```json
{
  "movie_id": 1, "title": "Interstellar (2014)", "genres": "Adventure|Drama|Sci-Fi",
  "score": 5.32, "normalized_score": 0.88,
  "recommendation_source": "hybrid",
  "vote_count": null,
  "reasons": ["Similar to movies you've enjoyed", "Liked by users with similar tastes"],
  "metadata": {"popularity_score": 0.8, "content_score": 2.8, "collaborative_score": 1.72}
}
```

**Semantic (from AI pipeline only — brute-force cosine, no normalize_scores applied):**
```json
{
  "movie_id": 1, "title": "Moon (2009)", "genres": "Drama|Sci-Fi",
  "score": 0.812
}
```

---

## Backend Files — Complete Reference

---

### `backend/main.py`

FastAPI app entry point. Registers all routers.

```python
app.include_router(auth_router,            prefix="/auth",  tags=["Authentication"])
app.include_router(users_router,                            tags=["Users"])
app.include_router(movies_router,                           tags=["Movies"])
app.include_router(ratings_router,                          tags=["Ratings"])
app.include_router(watchlist_router,                        tags=["Watchlist"])
app.include_router(recommendations_router,                  tags=["Recommendations"])
app.include_router(semantic_router)
app.include_router(ai_router)             # prefix="/ai",   tags=["AI"]
app.include_router(chat_router)           # prefix="/chat", tags=["Chat"]
```

Run with: `uvicorn main:app --reload` from `backend/`

---

### `backend/db/database.py`

- Builds PostgreSQL URL from `DATABASE_PASSWORD` env var
- Exports `engine` (SQLAlchemy), `SessionLocal`, and `DATABASE_URL` (string)
- Code uses `engine.connect()` with raw SQL text — not ORM sessions

---

### `backend/schemas/recommendation.py`

Canonical `Recommendation` Pydantic model (see Unified Movie Object Schema above).

---

### `backend/schemas/auth.py`

```python
class UserSignup(BaseModel): username, email, password
class UserLogin(BaseModel): email, password
```

### `backend/schemas/rating.py`
```python
class RatingCreate(BaseModel): movie_id: int, rating: float
```

### `backend/schemas/watchlist.py`
```python
class WatchlistCreate(BaseModel): movie_id: int
```

---

### `backend/utils/auth.py`

JWT authentication FastAPI dependency.

```python
def get_current_user(credentials: HTTPAuthorizationCredentials) → dict
```
- Decodes `Authorization: Bearer <token>` header
- Returns: `{"id": int, "username": str, "email": str}`
- Raises: `HTTPException(401)` on invalid/expired token

Used as `Depends(get_current_user)` on protected endpoints.

---

### `backend/api/auth.py`

```
POST /auth/signup  → hash pw, check uniqueness, INSERT users → {message}
POST /auth/login   → verify pw, create 24h JWT             → {access_token, token_type}
```

### `backend/api/users.py`
```
GET /me  (auth required) → {user: {id, username, email}}
```

### `backend/api/movies.py`
```
GET /movies                    → [{movie_id, title, genres}] (first 20)
GET /movies/search?query=<str> → [{movie_id, title, genres}] (ILIKE, limit 20)
```

### `backend/api/ratings.py`
```
POST /rate  (auth required)  Body: {movie_id, rating}  → {message}
```

### `backend/api/watchlist.py`
```
POST   /watchlist/add         (auth)  Body: {movie_id}   → {message}
GET    /watchlist             (auth)                      → [{movie_id, title, genres}]
DELETE /watchlist/{movie_id}  (auth)                      → {message}
```

### `backend/api/recommendations.py`
```
GET /recommendations          (auth)
  → calls recommendation_service.get_homepage_recommendations(user_id)
  → {must_watch, personalized, users_also_liked, hybrid}  (each has title + movies[])

GET /recommendations/content?movie_title=<str>
  → calls recommendation_service.get_content_based_recommendations(movie_title)
  → {title, movies[]}
```

### `backend/api/semantic.py`
```
GET /search/semantic?query=<str>&limit=10
  → calls SemanticService.search(query, limit)
  → {query, results: [{movie_id, title, genres, score}]}
```

### `backend/api/ai.py`
```
GET /ai/recommend?query=<str>
  Pipeline: parse_user_query → retrieve_candidates → rerank_movies → generate_explanation
  → {query, explanation, movies: [Recommendation x 10]}
```

### `backend/api/chat.py`
```
POST /chat/
  Body: ChatRequest {message: str, history: [{role, content}]}
  Pipeline: understand_user_intent → run_recommendation_pipeline → generate_explanation
  → {reply: str, movies: [Recommendation x 10]}
```

---

### `backend/services/recommendation_service.py`

```python
def get_homepage_recommendations(user_id: int) → dict
```
Calls recommenders in order and assembles 4-section response:
1. `popularity.get_popular_recommendations(user_id)` → `must_watch`
2. `hybrid.get_hybrid_recommendations(user_id)` → `personalized`
3. `collaborative.get_collaborative_recommendations(user_id)` → `users_also_liked`
4. `hybrid.get_hybrid_recommendations(user_id)` → `hybrid`

```python
def get_content_based_recommendations(movie_title: str) → dict
```
Wraps `content_based.get_similar_movies(movie_title)`.

---

### `backend/services/semantic_service.py`

```python
class SemanticService:
    @staticmethod
    def search(query: str, limit: int = 10) → List[dict]
```
Thin wrapper over `embeddings.semantic_search.semantic_search(query, limit)`.

---

### `backend/recommender/utils.py`

```python
def normalize_scores(recommendations: List[dict], score_field: str = "score") → List[dict]
```
Divides every item's score by the max score in the list, writing the result to `normalized_score`. Called at the end of every recommender function. Returns empty list unchanged.

---

### `backend/recommender/popularity.py`

```python
def get_popular_recommendations(user_id: int) → List[dict]
```
SQL: `ml_ratings JOIN movies`, exclude user-rated, `HAVING COUNT > 50`, `ORDER BY avg_rating DESC`, `LIMIT 20`.  
Appends `reasons: ["Highly rated by the community"]` and `metadata: {avg_rating}`.  
Calls `normalize_scores()` before returning.

---

### `backend/recommender/content_based.py`

```python
def get_similar_movies(movie_title: str) → List[dict]
```
Uses module-level `movies_df` and `similarity` matrix from `content_engine.py`.  
Exact title match → cosine similarity row → top 5 (excluding self).  
`reasons: ["Similar content and themes"]`, `vote_count: None`.  
Calls `normalize_scores()`.

---

### `backend/recommender/personalized_content.py`

```python
def get_personalized_recommendations(user_id: int, top_n: int = 20) → List[dict]
```
Fetches user's movies with `rating >= 4`, builds mean TF-IDF profile vector, computes cosine similarity against all movies, filters watched, returns top N.  
Cold start → returns `[]` if no qualifying ratings.  
`reasons: ["Matches your viewing preferences"]`.  
Calls `normalize_scores()`.

---

### `backend/recommender/collaborative.py`

**Module-level preprocessing (runs on import):** loads `ml_ratings`, builds user-movie matrix, applies `TruncatedSVD(n_components=50)`, computes user cosine similarity matrix.

```python
def get_collaborative_recommendations(user_id: int, top_n: int = 20) → List[dict]
```
Finds top 10 most similar users (excluding self), collects their `rating >= 4` movies not seen by target user, aggregates similarity scores per movie, returns top N.  
`reasons: ["Liked by users with similar tastes"]`.  
Calls `normalize_scores()`.

---

### `backend/recommender/hybrid.py`

```python
POPULARITY_WEIGHT = 0.2
CONTENT_WEIGHT    = 0.4
COLLABORATIVE_WEIGHT = 0.4

def get_hybrid_recommendations(user_id: int, top_n: int = 20) → List[dict]
```
Calls all three sub-recommenders. For each movie at rank `r` in source list: `weighted_score = (len(list) - r) * WEIGHT`. Aggregates by movie_id. Sorts by `hybrid_score`.  
Builds final output with sub-scores moved into `metadata`:
```python
metadata = {"popularity_score": ..., "content_score": ..., "collaborative_score": ...}
```
Generates `reasons` via `RecommendationExplainer.generate(movie)`.  
Calls `normalize_scores()`.

---

### `backend/recommender/engines/content_engine.py`

**Runs on import.** Loads `movies` + `tags` from DB, cleans genres, aggregates tags, stems with NLTK PorterStemmer, TF-IDF vectorizes (`max_features=5000`), computes full cosine similarity matrix.

Exports:
```python
movies_df   # pd.DataFrame — movie_id, title, genres, content
vectors     # np.ndarray — TF-IDF matrix (n_movies × 5000)
similarity  # np.ndarray — cosine similarity matrix (n_movies × n_movies)
```

---

### `backend/embeddings/embedding_service.py`

```python
class EmbeddingService:
    @classmethod
    def get_model() → SentenceTransformer   # lazy-loads all-MiniLM-L6-v2
    @classmethod
    def embed_text(text: str) → List[float] # 384-dim vector
```

---

### `backend/embeddings/semantic_search.py`

```python
def load_movie_embeddings() → pd.DataFrame
# SELECT m.movie_id, m.title, m.genres, me.embedding FROM movies JOIN movie_embeddings
# Returns: DataFrame [movie_id, title, genres, embedding]

def semantic_search(query: str, top_k: int = 10) → List[dict]
# Encodes query → cosine sim vs all embeddings → top K
# Returns: [{movie_id, title, genres, score}]
```

Note: brute-force scan — no ANN index. genres now included (added alongside Phase 2).

---

### `backend/explainability/recommendation_explainer.py`

```python
class RecommendationExplainer:
    @staticmethod
    def generate(movie: dict) → List[str]
```
Reads flat `content_score`, `collaborative_score`, `popularity_score` from an intermediate hybrid dict (before the final reshape). Returns up to 2 reasons for the top-scoring sources. Called only by `hybrid.py`.

---

### `backend/ai/llm_service.py`

**Single OpenAI wrapper — all LLM calls go through here.**

```python
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat(messages: list, temperature: float = 0.2) → str
# Calls gpt-4.1-mini, returns content string
```

---

### `backend/ai/schemas.py`

```python
class ParsedMovieQuery(BaseModel):
    genres: List[str] = []
    moods: List[str] = []
    themes: List[str] = []
    similar_to: List[str] = []   # specific movie titles
    exclude: List[str] = []

class AIRecommendationResponse(BaseModel):
    query: str
    explanation: str
    movies: list
```

---

### `backend/ai/query_parser.py`

```python
def parse_user_query(query: str) → ParsedMovieQuery
```
Sends query to LLM with structured JSON extraction prompt. Returns `ParsedMovieQuery()` (all empty lists) on any parse failure.

---

### `backend/ai/recommendation_pipeline.py`

```python
def retrieve_candidates(raw_query: str, parsed: ParsedMovieQuery) → List[dict]
```
Merges candidates from three sources (deduped by movie_id, up to 50 total):
1. `semantic_search(raw_query, top_k=20)` — always runs
2. `get_similar_movies(title)` for each title in `parsed.similar_to`
3. `get_popular_recommendations(user_id=0)` — popularity fallback (user_id=0 excludes nothing)

All wrapped in try/except so partial failures don't break the pipeline.

```python
def run_recommendation_pipeline(intent: str) → List[dict]
```
Single-call entry point for agents: `parse_user_query(intent)` → `retrieve_candidates(intent, parsed)` → `rerank_movies(intent, candidates)`.

---

### `backend/ai/reranker.py`

```python
def rerank_movies(query: str, candidates: List[dict], top_n: int = 10) → List[dict]
```
Sends candidate list as `movie_id: title | genres` lines to LLM. Asks for ranked JSON array of movie_ids. Reorders candidates by LLM rank, backfills any LLM-missed candidates, returns top N.  
Falls back to `candidates[:top_n]` on parse failure.

---

### `backend/ai/explanation_generator.py`

```python
def generate_explanation(query: str, movies: List[dict]) → str
```
Sends top-5 movies (title + genres) to LLM with the user query. LLM writes 2–3 sentences grounded in themes and tone. Falls back to a generic string on failure. Called by both `api/ai.py` and `agents/recommendation_agent.py`.

---

### `backend/agents/schemas.py`

```python
class ChatMessage(BaseModel): role: str, content: str
class ChatRequest(BaseModel): message: str, history: List[ChatMessage] = []
class ChatResponse(BaseModel): reply: str, movies: list = []
```

---

### `backend/agents/prompts.py`

```python
SYSTEM_PROMPT          # Agent persona — maintain context, refine across turns
INTENT_EXTRACTION_PROMPT  # "Convert this conversation into a standalone search query. Return ONLY the query."
```

---

### `backend/agents/chatbot.py`

```python
def understand_user_intent(message: str, history: List[dict]) → str
```
Builds full conversation (system prompt + history + current message) and appends `INTENT_EXTRACTION_PROMPT` as a second user message. The LLM sees the whole conversation and collapses it into a single standalone search string.

Example:
```
Turn 1: "Recommend sci-fi movies"
Turn 2: "Something darker"
Turn 3: "Not too old"
→ "dark sci-fi movies released after 2000"
```

---

### `backend/agents/recommendation_agent.py`

```python
def handle_chat(message: str, history: list) → dict
```
Orchestrates one chat turn:
1. `understand_user_intent(message, history)` → intent string
2. `run_recommendation_pipeline(intent)` → movies
3. `generate_explanation(intent, movies[:5])` → reply string
4. Returns `{"reply": str, "movies": List[dict][:10]}`

---

### `backend/scripts/`

| Script | Purpose |
|---|---|
| `seed_movies.py` | Load `movies.csv` → `movies` table |
| `seed_ratings.py` | Load `ratings.csv` → `ml_ratings` table |
| `seed_tags.py` | Load `tags.csv` → `tags` table |
| `generate_movie_embeddings.py` | Encode all movies with SentenceTransformer → upsert `movie_embeddings` |
| `test_db_connection.py` | psycopg2 connection sanity check |

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
| GET | `/ai/recommend?query=` | No | query param | `{query, explanation, movies}` |
| POST | `/chat/` | No | `{message, history[]}` | `{reply, movies}` |
| GET | `/` | No | — | `{message}` |

Auth header: `Authorization: Bearer <jwt_token>`

---

## Frontend Files — Complete Reference

---

### `frontend-react/src/api/api.js`

Central Axios client. `baseURL: '/api'`. Request interceptor adds JWT. Response interceptor redirects to `/auth` on 401.

```js
authAPI       = { signup(), login() }
moviesAPI     = { getAll(), search(q) }
recommendationsAPI = { getHomepage(), getContentBased(title) }
semanticAPI   = { search(query, limit=10) }
ratingsAPI    = { rate(movieId, rating) }
watchlistAPI  = { get(), add(movieId), remove(movieId) }
usersAPI      = { getMe() }
aiAPI         = { recommend(query) }         // GET /ai/recommend — 60s timeout
chatAPI       = { send(message, history) }   // POST /chat/     — 90s timeout
```

AI and chat endpoints have extended timeouts because they make multiple sequential LLM calls.

---

### `frontend-react/src/utils/movieUtils.js`

```js
getGenreGradient(genres) → CSS gradient string   // 16 genres mapped
getCleanTitle(title)    → str                    // removes year, fixes "The Matrix" article order
getYear(title)          → str | null
getGenres(genres)       → string[]               // splits pipe-separated string
formatScore(movie)      → {label, type} | null
  // vote_count truthy → {label: "★ X.X", type: "rating"}
  // normalized_score present → {label: "XX% Match", type: "match"}
  // neither → null (no score badge shown)
```

`formatScore` now uses `vote_count` as the discriminant (not `recommendation_source`), and `normalized_score` for the match percentage. This means the same function works for every recommendation source.

---

### `frontend-react/src/context/AuthContext.jsx`

State: `user` (`null` | `{id, username, email}`), `loading`.  
Methods: `login()`, `signup()`, `logout()`.  
Hook: `useAuth()`.

---

### `frontend-react/src/components/Navbar.jsx`

Nav links: **Home** `/`, **My List** `/watchlist`, **Browse** `/search`, **AI Picks** `/ai`, **Chat** `/chat`.  
"AI Picks" and "Chat" use gradient text (purple→red) to visually distinguish them.  
Also has: collapsible search bar → navigates to `/search?q=...`, user avatar + dropdown menu.

---

### `frontend-react/src/components/MovieCard.jsx`

Props: `{movie, onClick}`.  
Default: gradient bg, `formatScore()` badge, clean title + year + genre tags.  
Hover: play icon, title, genres, up to 2 `reasons` from the movie object.

---

### `frontend-react/src/components/MovieModal.jsx`

On mount: checks watchlist, fetches content-based "More Like This".  
Actions: add/remove watchlist, star rating (1–5), click similar movie opens new modal.

---

### `frontend-react/src/pages/Home.jsx`

`/` — protected. Calls `recommendationsAPI.getHomepage()`. Backend now handles all normalization, so no client-side score manipulation. Renders HeroBanner + 4 MovieRow sections.

---

### `frontend-react/src/pages/Search.jsx`

`/search` — protected. Debounced 380ms input. Keyword vs Semantic mode toggle. URL synced to `?q=`.

---

### `frontend-react/src/pages/Watchlist.jsx`

`/watchlist` — protected. Re-fetches on modal close.

---

### `frontend-react/src/pages/AIRecommend.jsx`

`/ai` — protected. Natural-language AI recommendations.

State: `query`, `result` (`{query, explanation, movies}`), `loading`, `error`, `selectedMovie`.

- Submit-on-enter form (no debounce — LLM calls are expensive)
- 4 example query chips for inspiration (only shown before first query)
- Three-dot animated loading indicator
- Results: explanation card (purple bordered, AI badge) + movie grid + "Ask something else" reset button
- Calls `aiAPI.recommend(query)` with 60s timeout

---

### `frontend-react/src/pages/Chat.jsx`

`/chat` — protected. Multi-turn conversational recommender.

State: `messages` (`[{id, role, content, movies[]}]`), `input`, `loading`, `selectedMovie`.

- Full-viewport layout — messages scroll, input pinned to bottom
- Empty state: chat icon + "What are you in the mood for?" + 4 starter chips
- Each AI message: gradient avatar dot + text bubble + horizontal movie strip (up to 6 cards)
- Loading: animated thinking dots in a bubble
- History sent to backend: `messages.map(m => ({role, content}))` — text only, not movies
- Context hint below input: "AI remembers this conversation — just say 'something darker'"
- Calls `chatAPI.send(message, history)` with 90s timeout

---

## Frontend Routing

| Route | Component | Protected |
|---|---|---|
| `/auth` | `Auth.jsx` | No |
| `/` | `Home.jsx` | Yes |
| `/search` | `Search.jsx` | Yes |
| `/watchlist` | `Watchlist.jsx` | Yes |
| `/ai` | `AIRecommend.jsx` | Yes |
| `/chat` | `Chat.jsx` | Yes |

JWT stored in `localStorage` under key `'token'`.

---

## Call Graph — Full Dependency Map

```
Browser
 └── React App
      ├── AuthContext → authAPI → POST /auth/*
      ├── ProtectedRoute → useAuth()
      │
      ├── Navbar (all pages)
      │    └── moviesAPI.search() → GET /movies/search
      │
      ├── Home (/)
      │    ├── recommendationsAPI.getHomepage() → GET /recommendations
      │    │    └── recommendation_service.py
      │    │         ├── popularity.py → SQL: ml_ratings + movies
      │    │         ├── hybrid.py
      │    │         │    ├── personalized_content.py → content_engine.py (TF-IDF) → SQL: movies + tags
      │    │         │    ├── collaborative.py (SVD) → SQL: ml_ratings
      │    │         │    └── recommendation_explainer.py
      │    │         └── collaborative.py
      │    └── MovieModal → getContentBased(), rate(), watchlist*
      │
      ├── Search (/search)
      │    ├── moviesAPI.search()   → GET /movies/search (keyword)
      │    └── semanticAPI.search() → GET /search/semantic
      │         └── semantic_service → semantic_search.py → SentenceTransformer + movie_embeddings
      │
      ├── Watchlist (/watchlist) → watchlistAPI.get() → GET /watchlist
      │
      ├── AIRecommend (/ai)
      │    └── aiAPI.recommend(query) → GET /ai/recommend
      │         └── api/ai.py
      │              ├── query_parser.py → llm_service → gpt-4.1-mini
      │              ├── recommendation_pipeline.py
      │              │    ├── semantic_search()
      │              │    ├── get_similar_movies() → content_engine.py
      │              │    └── get_popular_recommendations() → SQL
      │              ├── reranker.py → llm_service → gpt-4.1-mini
      │              └── explanation_generator.py → llm_service → gpt-4.1-mini
      │
      └── Chat (/chat)
           └── chatAPI.send(message, history) → POST /chat/
                └── api/chat.py
                     └── agents/recommendation_agent.py
                          ├── agents/chatbot.py → llm_service (intent extraction)
                          ├── ai/recommendation_pipeline.py (run_recommendation_pipeline)
                          │    ├── query_parser.py → llm_service
                          │    ├── retrieve_candidates() → semantic + content + popularity
                          │    └── reranker.py → llm_service
                          └── explanation_generator.py → llm_service
```

Each chat turn makes **3 LLM calls**: intent extraction, reranking, explanation.  
Each `/ai/recommend` call makes **3 LLM calls**: parsing, reranking, explanation.

---

## Recommendation Algorithm Reference

| Algorithm | File | Input | Data Source | Output |
|---|---|---|---|---|
| Popularity | `popularity.py` | user_id | `ml_ratings` | Top-rated movies (count > 50), normalized |
| Content-Based | `content_based.py` | movie_title | content_engine | Top 5 similar, normalized |
| Personalized | `personalized_content.py` | user_id | `ratings` + content_engine | Profile-matched, normalized |
| Collaborative SVD | `collaborative.py` | user_id | `ml_ratings` | Similar-user picks, normalized |
| Hybrid | `hybrid.py` | user_id | All three above | Weighted ensemble, normalized |
| Semantic | `semantic_search.py` | query string | `movie_embeddings` | Cosine sim to query (no normalize_scores) |
| AI Pipeline | `recommendation_pipeline.py` | intent string | semantic + content + popularity | LLM-reranked candidates |

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
| AI candidate pool size | 50 | `recommendation_pipeline.py` |
| AI reranker top-N | 10 | `reranker.py` |
| LLM model | gpt-4.1-mini | `llm_service.py` |
| LLM temperature (parsing/ranking) | 0.2 | `llm_service.py` default |
| LLM temperature (explanation) | 0.4 | `explanation_generator.py` |
| LLM temperature (intent extraction) | 0.1 | `chatbot.py` |

---

## Known Gaps / Next Steps

1. **Vector DB** — semantic search is a brute-force cosine scan over all embeddings. Should migrate to `pgvector` or Pinecone for ANN search at scale.

2. **Cold start** — new users with no ratings get empty personalized/collaborative rows. Consider falling back to popularity automatically.

3. **CORS** — not configured in `main.py`. Required before deploying frontend and backend on separate origins.

4. **Deployment** — Planned: React on Vercel, FastAPI on Render/Railway, cloud PostgreSQL (Neon URL already in `.env`).

5. **Module-level preprocessing** — `content_engine.py` and `collaborative.py` run heavy ML on import, making the first server startup slow. Consider background startup tasks.

6. **User preference memory** — chat has no persistent memory between sessions. A `user_preferences` table (favourite_genres, disliked_genres etc.) would let the agent incorporate long-term preferences automatically.

7. **AI endpoint authentication** — `/ai/recommend` and `/chat/` are currently unauthenticated. Adding `Depends(get_current_user)` would allow user-specific context (e.g. excluding already-watched movies from AI results).

8. **LLM cost & latency** — each chat turn and AI recommendation makes 3 sequential GPT calls (~15–30s total). Candidates for optimization: cache parsed queries, parallelize reranker + explanation, use streaming for chat replies.
