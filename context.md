# Movie Recommender System — Project Context

# Vision

This project aims to build a production-style movie recommendation platform inspired by systems used by Netflix, Spotify, YouTube, and Amazon.

The long-term goal is to progressively evolve the system from:

1. Popularity-based recommendations
2. Content-based filtering
3. Collaborative filtering
4. Hybrid recommendation systems
5. Semantic embeddings + AI conversational recommender
6. Fully deployed production architecture

The project is intentionally being built in layers to learn:

* backend engineering
* recommender systems
* ML systems
* vector search
* MLOps
* frontend engineering
* production deployment

---

# Current Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pandas
* scikit-learn
* psycopg2

---

## Frontend

Current:

* React 18
* Vite 5
* React Router DOM v6
* Axios

Prototype (kept for reference):

* Streamlit (`frontend/`)

Planned:

* Next.js (optional — for SSR/SEO)

---

## ML / Recommendation

* TF-IDF Vectorization
* Cosine Similarity
* TruncatedSVD
* Hybrid Recommendation Systems

---

## Database

PostgreSQL

---

# Dataset

Using:
MovieLens `ml-latest-small`

Files:

* movies.csv
* ratings.csv
* tags.csv

---

# Project Structure

```text
movie-recommender/

├── backend/
│
│   ├── api/
│   ├── db/
│   ├── models/
│   ├── recommender/
│   │
│   │   ├── engines/
│   │   ├── popularity.py
│   │   ├── content_based.py
│   │   ├── personalized_content.py
│   │   ├── collaborative.py
│   │   ├── hybrid.py
│   │
│   ├── services/
│   ├── utils/
│
├── frontend/                  # Streamlit prototype (Python)
├── frontend-react/            # React app (current)
│
│   ├── src/
│   │   ├── api/api.js
│   │   ├── components/
│   │   │   ├── HeroBanner.jsx
│   │   │   ├── MovieCard.jsx
│   │   │   ├── MovieModal.jsx
│   │   │   ├── MovieRow.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── ProtectedRoute.jsx
│   │   ├── context/AuthContext.jsx
│   │   ├── pages/
│   │   │   ├── Auth.jsx
│   │   │   ├── Home.jsx
│   │   │   ├── Search.jsx
│   │   │   └── Watchlist.jsx
│   │   └── utils/movieUtils.js
│   ├── index.html
│   └── vite.config.js
│
├── data/
├── notebooks/
├── docker/
└── README.md
```

---

# Architectural Philosophy

The project intentionally separates:

* API Layer
* Service Layer
* Recommendation Layer
* ML Engine Layer

This mirrors real production recommendation systems.

---

# Layer Responsibilities

## API Layer

Folder:

```text
api/
```

Responsibilities:

* HTTP routes
* request handling
* authentication
* query params

Contains:

* auth.py
* users.py
* ratings.py
* watchlist.py
* recommendations.py

---

## Service Layer

Folder:

```text
services/
```

Responsibilities:

* orchestration
* combining recommenders
* homepage assembly

Main file:

```text
recommendation_service.py
```

---

## Recommender Layer

Folder:

```text
recommender/
```

Responsibilities:

* recommendation algorithms
* ranking logic
* recommendation scoring

Contains:

* popularity.py
* content_based.py
* personalized_content.py
* collaborative.py
* hybrid.py

---

## Engine Layer

Folder:

```text
recommender/engines/
```

Responsibilities:

* preprocessing
* vectorization
* embeddings
* similarity matrices
* ML pipelines

Contains:

* content_engine.py

Future:

* embedding_engine.py
* semantic_engine.py

---

# Database Design

## users

```sql
id
username
email
password_hash
created_at
```

---

## movies

```sql
movie_id
title
genres
```

---

## ratings

Stores:
real user ratings

```sql
id
user_id
movie_id
rating
created_at
```

---

## ml_ratings

Stores:
MovieLens dataset ratings

Used for:

* popularity recommender
* collaborative filtering

```sql
user_id
movie_id
rating
timestamp
```

---

## tags

Stores:
MovieLens tags

Used for:
content-based filtering

```sql
user_id
movie_id
tag
timestamp
```

---

## watchlist

```sql
id
user_id
movie_id
created_at
```

---

# Authentication System

Implemented:

* signup
* login
* JWT authentication

Protected routes use:

```python
Depends(get_current_user)
```

Secret key stored in:
`.env`

---

# APIs Implemented

## Auth

```text
POST /auth/signup
POST /auth/login
```

---

## User

```text
GET /me
```

---

## Movies

```text
GET /movies
GET /movies/search
```

---

## Ratings

```text
POST /rate
```

---

## Watchlist

```text
POST /watchlist/add
GET /watchlist
POST /watchlist/remove
```

---

## Recommendations

```text
GET /recommendations
GET /recommendations/content
```

---

# Recommendation Systems

# 1. Popularity-Based Recommender

File:

```text
recommender/popularity.py
```

Logic:

* aggregate ratings
* average movie scores
* minimum rating threshold
* exclude already rated movies

Used for:

```text
🔥 Must Watch
```

---

# 2. Content-Based Filtering

File:

```text
recommender/content_based.py
```

Engine:

```text
recommender/engines/content_engine.py
```

Pipeline:

1. Load movies + tags
2. Clean genres
3. Aggregate tags
4. Merge datasets
5. Build content column
6. Lowercase text
7. Stem text using NLTK PorterStemmer
8. TF-IDF Vectorization
9. Cosine Similarity

Used for:

```text
🎭 More Like This
```

---

# 3. Personalized Content Recommender

File:

```text
recommender/personalized_content.py
```

Logic:

* analyze user watch history
* fetch similar movies
* aggregate recommendations
* remove duplicates
* exclude watched movies

Used for:

```text
🎭 Personalized Content
```

---

# 4. Collaborative Filtering

File:

```text
recommender/collaborative.py
```

Uses:

* User-Movie Matrix
* Sparse Matrix
* TruncatedSVD
* Cosine Similarity

Matrix factorization equation:

R ≈ UΣVᵀ

Pipeline:

1. Build user-movie matrix
2. Apply SVD
3. Learn latent embeddings
4. Find similar users
5. Recommend highly-rated unseen movies

Used for:

```text
👥 Users Also Liked
```

---

# 5. Hybrid Recommender

File:

```text
recommender/hybrid.py
```

Combines:

* popularity
* content-based
* collaborative filtering

Current weights:

```python
POPULARITY_WEIGHT = 0.2
CONTENT_WEIGHT = 0.4
COLLABORATIVE_WEIGHT = 0.4
```

Outputs:

```text
🧠 Personalized For You
```

This is an ensemble recommendation system.

---

# Homepage Architecture

Goal:
Netflix-style homepage.

Structure:

```text
------------------------------------------------
Search Bar
------------------------------------------------

🔥 Must Watch

[Movie Cards]

------------------------------------------------

🎭 More Like Interstellar

[Movie Cards]

------------------------------------------------

👥 Users Also Liked

[Movie Cards]

------------------------------------------------

🧠 Personalized For You

[Movie Cards]

------------------------------------------------
```

---

# Recommendation Service Layer

Main orchestrator:

```text
services/recommendation_service.py
```

Purpose:
assemble recommendation rows.

Current sections:

* must_watch
* personalized
* users_also_liked

Future:

* trending
* continue watching
* because you watched
* AI generated recommendations

---

# Frontend

Current (React — `frontend-react/`):

* React 18 + Vite 5
* React Router DOM v6 for client-side routing
* Axios for API communication
* AuthContext for JWT session management
* Netflix-style homepage (HeroBanner, MovieRow, MovieCard)
* MovieModal for movie detail overlay
* Auth page (login / sign up)
* Search page
* Watchlist page
* ProtectedRoute for guarding authenticated routes

Remaining frontend work:

* hover previews / trailer embeds
* semantic AI search bar
* conversational recommender chatbot

Planned (optional):

* Next.js migration for SSR/SEO

---

# AI + Embedding Roadmap

Future architecture includes:

## Semantic Embeddings

Using:

* sentence transformers
* OpenAI embeddings
* vector databases

Will enable:

* semantic search
* "find movies like..."
* natural language recommendation

---

## Conversational Recommender Agent

Planned:
AI chatbot interface.

Examples:

* "Recommend mind-bending sci-fi movies"
* "Movies like Interstellar but darker"
* "Funny movies for family night"

---

# Deployment Roadmap

Planned:

* React frontend on Vercel
* FastAPI backend on Render/Railway
* PostgreSQL cloud deployment

Future:

* Docker
* Kubernetes
* Airflow
* ML pipelines
* CI/CD

---

# Engineering Principles

This project intentionally prioritizes:

* layered architecture
* clean separation of concerns
* scalable recommender design
* production-style backend structure
* iterative development

Avoided intentionally in Phase 1:

* microservices
* Kubernetes
* premature optimization
* overengineering

Goal:
build a working vertical slice first.

---

# Long-Term Goal

Build a fully production-style AI recommendation platform with:

* hybrid recommendation systems
* embeddings
* conversational AI
* vector search
* real frontend
* scalable backend
* MLOps infrastructure
* deployment pipelines

The project serves as:

* a deep learning platform
* portfolio project
* recommender systems lab
* full-stack ML engineering project
