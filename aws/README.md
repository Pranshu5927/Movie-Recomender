# AWS Infrastructure & Deployment

This directory contains all AWS-related files, configurations, and setup scripts for deploying the Movie Recommender application to production.

## Files in This Directory

### Setup & Documentation
| File | Purpose |
|------|---------|
| `PHASE1-AWS-ACCOUNT-SETUP.md` | **START HERE** — Step-by-step guide to create AWS account, IAM user, and generate GitHub Secrets |
| `iam-policy.json` | IAM permissions policy for the `github-actions-deployer` user (defines what GitHub Actions can do in AWS) |
| `infrastructure-notes.md` | Notes on manual AWS console steps for ECR, RDS, ECS setup (will be created in Phase 4) |
| `secrets-setup.sh` | Script to create AWS Secrets Manager entries (will be created in Phase 5) |

### CloudFormation (Infrastructure as Code)
These files let you create entire AWS infrastructure with one command instead of clicking AWS console.

| File | Purpose |
|------|---------|
| `cloudformation-template.yaml` | Single file that defines: ECR, RDS, ECS cluster, ALB, security groups (will be created in Phase 4) |

### Shell Scripts (Automation)
These scripts automate AWS setup to avoid manual console clicks.

| File | Purpose |
|------|---------|
| `ecr-setup.sh` | Creates ECR repositories for backend + frontend images (will be created in Phase 4) |
| `rds-setup.sh` | Creates RDS PostgreSQL database (will be created in Phase 4) |
| `ecs-cluster.sh` | Creates ECS cluster and registers task definitions (will be created in Phase 4) |
| `cleanup.sh` | Deletes all AWS resources to stop billing (will be created in Phase 4) |

## Deployment Flow

```
Your Code (GitHub)
    ↓
GitHub Actions (CI/CD Pipeline)
    ↓ (builds Docker images)
ECR (Image Registry)
    ↓ (pulls latest image)
ECS (Runs containers)
    ↓ (talks to)
RDS PostgreSQL (Database)
```

## Quick Start

### Phase 1: AWS Setup (You are here)
1. Read: `PHASE1-AWS-ACCOUNT-SETUP.md`
2. Follow steps to:
   - Create AWS account
   - Create IAM user
   - Add GitHub Secrets

✅ This takes ~30 minutes

### Phase 2-3: Docker & GitHub Actions
- Create `backend/Dockerfile`, `frontend-react/Dockerfile`, `docker-compose.yml`
- Create `.github/workflows/ci-cd.yml`
- Test locally, then GitHub Actions can deploy

### Phase 4: AWS Infrastructure
- Use CloudFormation or shell scripts to create:
  - ECR (image storage)
  - RDS (database)
  - ECS (container orchestrator)
  - ALB (load balancer)

### Phase 5+: Production Deployment
- Push code → GitHub Actions builds & deploys automatically
- Monitor with CloudWatch

## AWS Services Used

| Service | Purpose | Free Tier? | Cost |
|---------|---------|-----------|------|
| **ECR** | Store Docker images | Partial (50GB/month free) | $0-2 |
| **ECS Fargate** | Run containers | Partial (160 hours/month free) | $5-10 |
| **RDS PostgreSQL** | Database | Partial (750 hours/month free) | $8-15 |
| **ALB** | Load balancer | Partial | $5-8 |
| **CloudWatch** | Logs & monitoring | Partial | $0-5 |
| **Secrets Manager** | Secret storage | Pay per secret | ~$1 |
| **Total (estimated)** | — | — | **$18-38/month** |

**Goal**: Stay under $30/month by maximizing free tier.

## Key Concepts

### ECR (Elastic Container Registry)
- Stores your Docker images (backend + frontend)
- GitHub Actions builds images and pushes them here
- ECS pulls images from ECR to run

### RDS (Relational Database Service)
- Managed PostgreSQL (AWS handles backups, updates, scaling)
- Persists user data, ratings, watchlist
- Accessible by ECS containers via connection string

### ECS (Elastic Container Service)
- Runs your Docker containers
- Fargate = serverless (you don't manage servers)
- Launches containers from ECR images
- Integrates with ALB for load balancing

### ALB (Application Load Balancer)
- Routes traffic to ECS containers
- Handles SSL/TLS encryption
- Distributes load across multiple replicas

### GitHub Actions
- CI/CD pipeline
- Runs tests, builds Docker images, pushes to ECR
- Triggers ECS to deploy new version

## Environment Variables & Secrets

### GitHub Secrets (for CI/CD)
- `AWS_ACCESS_KEY_ID` — credentials for GitHub Actions
- `AWS_SECRET_ACCESS_KEY` — credentials for GitHub Actions
- `AWS_REGION` — which AWS region to use (us-east-1)

### AWS Secrets Manager (for Production)
- `OPENAI_API_KEY` — stored securely in AWS
- `DATABASE_PASSWORD` — ECS reads this at runtime
- `SECRET_KEY` — JWT secret for auth

## Troubleshooting

| Problem | Solution |
|---------|----------|
| GitHub Actions fails with "access denied" | Check GitHub Secrets are set correctly in Settings → Secrets |
| ECR image not updating | Check that GitHub Actions workflow is pushing to ECR |
| ECS containers can't reach database | Check RDS security group allows ECS security group |
| Billing is high | Check for forgotten resources (old databases, ALBs). Use `cleanup.sh` |

## Next Steps

1. **Right now**: Read `PHASE1-AWS-ACCOUNT-SETUP.md` and complete it
2. **After Phase 1**: We'll create Dockerfiles and test locally
3. **After Phase 3**: We'll set up AWS infrastructure using these scripts

---

**Questions?** Each file has detailed comments explaining what's happening and why.
