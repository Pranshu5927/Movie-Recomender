# Movie Recommender

A movie recommendation system scaffold for building an end-to-end ML project.

## Project layout

- `backend/` — API, model training, and recommendation engine logic
- `frontend/` — user interface and web app
- `data/` — raw and processed datasets
- `notebooks/` — exploratory analysis and model development notebooks
- `docker/` — Docker configuration files and deployment assets
- `requirements.txt` — Python dependencies
- `.gitignore` — files and directories to exclude from version control

## Getting started

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your movie dataset files under `data/` and start building the backend and frontend.
