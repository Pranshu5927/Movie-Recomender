# Phase 3: GitHub Actions CI/CD Pipeline

**Goal**: Automatically test every change and build/push Docker images to AWS ECR whenever code is merged to `main`.

**Time**: ~2 hours (including watching your first few pipeline runs and fixing any red X's)

**What You'll Have at the End**:
- Every Pull Request automatically runs the backend test suite against a real Postgres database
- Every merge to `main` automatically builds the backend + frontend Docker images and pushes them to AWS ECR
- A foundation ready for Phase 4 (ECS will pull these images)

---

## What We Created

| File | Purpose |
|------|---------|
| `.github/workflows/ci-cd.yml` | The pipeline definition: `test` job + `build-and-push` job |
| `backend/pytest.ini` | Tells pytest where to find tests and how to set up the Python path |
| `backend/tests/test_api.py` | 5 tests covering health check, signup/login, and the movies endpoint |
| `requirements.txt` (updated) | Added `pytest`, switched `torch` to the CPU-only wheel |

### Architecture

```
Developer pushes code
       │
       ▼
┌─────────────────────────┐
│  Pull Request → main     │
│  ─────────────────────   │
│  Job: test                │
│   ├─ Spin up Postgres     │
│   ├─ pip install deps     │
│   ├─ Load schema.sql      │
│   └─ Run pytest            │
└─────────────────────────┘
       │  (merge)
       ▼
┌─────────────────────────┐
│  Push → main              │
│  ─────────────────────   │
│  Job: build-and-push       │
│   ├─ Login to AWS ECR      │
│   ├─ Create ECR repos      │
│   │   (if missing)         │
│   ├─ Build backend image   │
│   ├─ Build frontend image  │
│   └─ Push both → ECR        │
│       (tags: latest, SHA)   │
└─────────────────────────┘
       │
       ▼
   AWS ECR (ready for Phase 4 ECS)
```

---

## Step 1: Commit the Pending Phase 3 Files

A previous session already created `backend/pytest.ini`, `backend/tests/test_api.py`, and updated `requirements.txt` (added `pytest`), but they were never committed. This phase adds the workflow file and the CPU-only torch tweak on top.

```bash
cd path/to/Movie-Recommender

git add requirements.txt backend/pytest.ini backend/tests/ .github/workflows/ci-cd.yml aws/PHASE3-CICD-SETUP.md
git commit -m "Phase 3: Add CI/CD pipeline (test + build/push to ECR)"
```

**Recommended**: push to a feature branch first and open a Pull Request, rather than committing straight to `main`. This lets you see the `test` job run safely — the `build-and-push` job only runs on a push to `main`, so a PR won't try to push images yet.

```bash
git checkout -b phase3-cicd
git push -u origin phase3-cicd
```

Then open a PR on GitHub from `phase3-cicd` → `main`.

---

## Step 2: Open a PR and Watch the `test` Job Run

### 2.1 Find the Pipeline Run
- Go to your repo on GitHub → **Pull Requests** tab → open your new PR
- Scroll down to the **checks** section, or click the **"Actions"** tab at the top of the repo
- Click on the running workflow ("CI/CD Pipeline")

### 2.2 What Each Step Does
| Step | What's Happening | Expected Time |
|------|-------------------|----------------|
| Checkout code | Clones your repo into the runner | ~5s |
| Set up Python | Installs Python 3.11, restores pip cache if available | ~10-30s |
| Install system dependencies | `apt-get install gcc libpq-dev` (needed for psycopg2) | ~10-20s |
| Install Python dependencies | `pip install -r requirements.txt` — **slowest step** | 3-8 min (first run), faster on cache hits |
| Load database schema | Runs `schema.sql` against the Postgres service container | ~2s |
| Run tests | `pytest` — runs the 5 tests in `backend/tests/test_api.py` | ~10-30s |

**First run will be slow** because there's no pip cache yet. The CPU-only torch wheel (~150-200MB) instead of the default CUDA build (~2GB+) keeps this from being painfully slow.

### 2.3 If It's Red (Failed)
Check the **Troubleshooting** table below — the most common first-run issues are missing env vars (`OPENAI_API_KEY`, `SECRET_KEY`) or the Postgres service not being ready yet.

---

## Step 3: Merge to `main` and Watch `build-and-push` Run

### 3.1 Merge the PR
Once the `test` check is green, merge the PR into `main`.

### 3.2 Watch the Second Job
- Go to the **Actions** tab → click the new workflow run (triggered by the merge commit)
- You'll now see **two** jobs: `test` (runs again) and `build-and-push` (new)
- `build-and-push` only starts after `test` succeeds (`needs: test`) and only runs because this is a `push` to `main` (`if: github.event_name == 'push' && github.ref == 'refs/heads/main'`)

### 3.3 What Each Step Does
| Step | What's Happening |
|------|-------------------|
| Configure AWS credentials | Uses your Phase 1 GitHub Secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`) to authenticate |
| Login to Amazon ECR | Logs Docker into your private ECR registry; also gives us the registry URL |
| Set up Docker Buildx | Enables advanced Docker build features (used for caching) |
| Create ECR repositories if they don't exist | First run: creates `movie-recommender-backend` and `movie-recommender-frontend` repos. Later runs: no-op |
| Build and push backend image | Builds `backend/Dockerfile`, tags it `latest` and `<git-sha>`, pushes both to ECR |
| Build and push frontend image | Same, for `frontend-react/Dockerfile` |

**First run will take a while** (building both images from scratch). Subsequent runs are faster thanks to `cache-from`/`cache-to: type=gha` (GitHub Actions caches Docker layers).

---

## Step 4: Verify Images in ECR

1. Log into the [AWS Console](https://console.aws.amazon.com)
2. Make sure you're in the **us-east-1** region (top-right region selector)
3. Search for **"ECR"** (Elastic Container Registry) in the top search bar
4. Click **"Repositories"** in the left sidebar
5. You should see two repositories:
   - `movie-recommender-backend`
   - `movie-recommender-frontend`
6. Click into either one → **"Images"** tab
7. You should see at least two image tags: `latest` and a long hex string (the git commit SHA)

---

## What's Happening Under the Hood

### Why `OPENAI_API_KEY` and `SECRET_KEY` dummy values?
`backend/main.py` imports every API router, including `api/ai.py` → `ai/llm_service.py`, which runs this at **module import time**:
```python
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```
If `OPENAI_API_KEY` is unset, this line raises an error the moment `main` is imported — before any test even runs. The tests never call the real OpenAI API, so a dummy string like `sk-test-dummy-key-for-ci` is enough to satisfy the constructor.

Similarly, `backend/utils/auth.py` reads `SECRET_KEY` to sign/verify JWTs during the signup/login tests — it just needs to be *some* non-empty string.

### Why a Postgres service container?
`backend/tests/test_api.py` hits real endpoints that talk to the database (`/auth/signup`, `/auth/login`, `GET /movies`). The `services:` block in the workflow spins up a throwaway `postgres:15-alpine` container alongside the test job, exposed on `localhost:5432`. We then run `backend/db/schema.sql` against it to create the empty tables — matching what `test_movies_endpoint_with_empty_db` expects (`GET /movies` → `[]`).

### Why `aws-actions/amazon-ecr-login`'s `outputs.registry`?
Every ECR image lives at a URL like `<your-account-id>.dkr.ecr.us-east-1.amazonaws.com/<repo-name>`. Rather than hardcoding your 12-digit AWS account ID anywhere (even as a secret), the ECR login action derives it from your credentials at runtime and exposes it as `steps.ecr-login.outputs.registry`. The build steps reference this directly.

### Why `cache-from`/`cache-to: type=gha`?
Docker builds happen layer-by-layer. The `pip install -r requirements.txt` layer is the most expensive part of the backend image. GitHub Actions cache (`type=gha`) persists these layers between workflow runs, so if `requirements.txt` hasn't changed, that layer is reused instead of rebuilt.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `pip install` takes 8+ minutes on every run | Cache only helps after the first successful run on a branch. Confirm `cache-dependency-path: requirements.txt` matches the file you're editing. |
| `OpenAIError: The api_key client option must be set` | The `Run tests` step's `env:` block is missing `OPENAI_API_KEY`. Check it's set to a non-empty dummy string. |
| `psycopg2.OperationalError: connection to server ... refused` | The Postgres service container wasn't ready. Confirm the `services.postgres.options` health-check block is present — GitHub Actions won't start job steps until it passes. |
| `relation "movies" does not exist` | The "Load database schema" step didn't run or failed silently. Check its logs — `psql` needs `PGPASSWORD` set and `-h localhost -U postgres -d movie_recommender`. |
| ECR login fails with `AccessDenied` | Double-check the `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` GitHub Secrets are correct and the IAM user still has the policies from `aws/iam-policy.json`. |
| `psql: command not found` | Shouldn't happen on `ubuntu-latest` (psql client is preinstalled), but if it does, add `sudo apt-get install -y postgresql-client` before the schema step. |
| `build-and-push` didn't run after merging | Check it only triggers on `push` to `main` — if you merged via "squash and merge" it should still count as a push event. If you used a different default branch name, update `branches: [main]`. |

---

## Success Checklist

- ✅ PR shows a green `test` check (all 5 backend tests pass)
- ✅ Merging to `main` triggers `build-and-push`
- ✅ `movie-recommender-backend` and `movie-recommender-frontend` repos exist in ECR
- ✅ Each repo has a `latest` tag and a tag matching the merge commit's SHA
- ✅ No secrets (API keys, passwords) appear anywhere in the workflow file or logs

---

## Key Concepts Learned

1. **CI vs CD**: CI (`test` job) catches bugs before merge. CD (`build-and-push` job) automates getting your code into a deployable artifact (a Docker image in ECR).
2. **Service containers**: GitHub Actions can spin up throwaway dependencies (like Postgres) just for the duration of a job.
3. **Dependency caching**: Both `pip` and Docker layer caches dramatically speed up repeat CI runs.
4. **Container registries**: ECR is just a private, AWS-hosted version of Docker Hub — it stores the images that ECS will later run.
5. **Idempotent infrastructure**: The "create ECR repos if they don't exist" step can run every time without error — first run creates, every run after that is a no-op.
6. **Image tagging strategy**: `latest` is convenient for humans; the git SHA tag (`${{ github.sha }}`) gives you an exact, traceable artifact for every commit — useful for rollbacks later.

---

## Next Steps

✅ Pipeline tests every PR and pushes images to ECR on merge
✅ ECR repositories now exist and are ready to be referenced by ECS

**Next Phase**: Phase 4 — AWS Infrastructure (ECR is done; now add RDS PostgreSQL, ECS cluster/task definitions, and an ALB)
- The `TODO (Phase 4/7)` comment at the bottom of `ci-cd.yml` marks where the ECS deploy step will be added once the cluster and task definitions exist.

---

## Quick Reference

```bash
# Push your branch and open a PR
git push -u origin phase3-cicd

# After merging, watch the pipeline
# GitHub repo → Actions tab → latest "CI/CD Pipeline" run

# List images in a repo from the CLI
aws ecr describe-images --repository-name movie-recommender-backend --region us-east-1
aws ecr describe-images --repository-name movie-recommender-frontend --region us-east-1
```

| Item | Value |
|------|-------|
| ECR Repos | `movie-recommender-backend`, `movie-recommender-frontend` |
| Image Tags | `latest`, `<git-sha>` |
| Region | `us-east-1` |
| Workflow File | `.github/workflows/ci-cd.yml` |
