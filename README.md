# Movie API — Monorepo Overview

This repository implements a movie API and related infrastructure components. The repo uses a multi-branch structure where each branch encapsulates a focused area of the project (backend, frontend/gateway, deployment, observability, infra, images, etc.). This README consolidates information across all branches and serves as the canonical entry point for developers and operators.

Last updated: 2026-01-30
Author: pokerface03 

Table of contents
- Project summary
- Branch layout and purpose
- Architecture overview
- Features
- Quick start (local, Docker, Kubernetes)
- Environment variables and configuration
- Databases and caching
- Observability (logging, metrics, alerts)
- CI/CD and images
- Branch-specific notes and how to locate branch docs


Project summary
This repository contains a RESTful Movie API service along with infrastructure-as-code, observability and deployment tooling. The repo is organized as a monorepo-like collection of branches that focus development and documentation on a single concern per branch (for example, `deployment/kubernetes` holds k8s cluster configuration, `infa/terraform` has terraform modules, etc.).

Branch layout and purpose
(Branches discovered in the repository — use these names to find branch-specific content or artifacts)
- APM/Logstash — logging pipeline and Logstash configuration
- CI/CD — continuous integration and deployment pipeline definitions
- backend/restAPI — backend service implementation (API)
- config/Prometheus — Prometheus configuration and scrape rules
- database/postgress — PostgreSQL schema, migrations, and DB config
- database/redis — Redis config and caching patterns
- deployment/dockerize — Dockerfile(s) and containerization notes
- deployment/kubernetes — Kubernetes cluster
- filters/matrix — domain filters or matrix processing (search/filters)
- frontend/gateway — frontend gateway, API gateway, or reverse proxy configuration
- frontent/development — frontend development branch
- images/ECR — Docker image build and ECR push scripts
- infa/terraform — Terraform modules and deployment automation
- logging/alertmanager — Alertmanager config for Prometheus alerts
- logging/elasticSearch — Elasticsearch indices and ingestion config
- main — canonical runtime code / default branch for releases

Architecture overview
- Service tiering:
  - Backend: Movie REST API (CRUD, search, filters)
  - Frontend/gateway: Gateway or UI that proxies to the backend
  - Database: Postgres (branch present) or MongoDB (if used; update as applicable)
  - Cache: Redis (caching and rate-limiting)
- Deployment:
  - Container images built and stored in ECR (images/ECR)
  - Deployable to Kubernetes (deployment/kubernetes) with Docker builds in deployment/dockerize
  - Terraform to provision infra (infa/terraform)
- Observability & logging:
  - Metrics via Prometheus (config/Prometheus)
  - Alerts via Alertmanager (logging/alertmanager)
  - Centralized logging with Logstash/Elasticsearch (APM/Logstash & logging/elasticSearch)

Features
- RESTful API: CRUD operations for movies
- Filtering and matrix-based search (filters/matrix)
- Pagination and sorting
- Optional authentication (JWT hooks can be applied)
- Logging, metrics, and alerting built into infra branches
- Containerized builds and K8s manifests for production-grade deployments

Quick start

Prerequisites
- Node.js (or runtime depending on backend implementation)
- Docker (if using containers)
- kubectl 
- Terraform (if deploying infra from repo)
- A database: Postgres and/or Redis (local or remote)

Local development (generic)
1. Clone the repository:
   ```bash
   git clone https://github.com/pokerface03/movie-api.git
   cd movie-api
   ```
2. Checkout the backend implementation branch if present:
   ```bash
   git checkout backend/restAPI
   ```
3. Install dependencies and run:
   ```bash
   npm install
   npm run dev
   # or the project-specific commands in backend/restAPI
   ```
4. Configure environment variables (see below).

Docker
- Build the image (branch: deployment/dockerize or images/ECR):
  ```bash
  docker build -t movie-api:latest .
  ```
- Run with local DB:
  ```bash
  docker run --env-file .env -p 3000:3000 movie-api:latest
  ```

Kubernetes
- minikube was used for the deployment of kubernetes 

Environment variables (example)
Create a `.env` with the variables the service expects. Replace values according to the branch-specific implementation (backend/restAPI).
```
PORT=3000
NODE_ENV=development
DATABASE_URL=postgres://user:pass@localhost:5432/movie_api
REDIS_URL=redis://localhost:6379
JWT_SECRET=change_this
LOG_LEVEL=info
```

Databases and caching
- PostgreSQL: migrations and schema in `database/postgress` branch
- Redis: caching patterns and configuration present in `database/redis`
- If your backend uses a different DB (MongoDB), update DATABASE_URL accordingly and provide migration scripts if needed

Observability and logging
- Prometheus configs and scrape rules: `config/Prometheus`
- Alerting rules and Alertmanager config: `logging/alertmanager`
- Centralized logging and pipelines: `APM/Logstash` and `logging/elasticSearch`

CI/CD and images
- CI/CD definitions (pipelines) live in the `CI/CD` branch
- Container images and ECR push scripts: `images/ECR`
- Typical pipeline steps:
  - Lint & test
  - Build docker image and push to ECR


Branch-specific notes
- Many branch READMEs are placeholders. Use this consolidated README as the main reference;

How to find branch-level docs and artifacts
- To view a branch in GitHub: https://github.com/pokerface03/movie-api/tree/<branch-name>
- Example: Prometheus config on branch `config/Prometheus`:
  https://github.com/pokerface03/movie-api/tree/config/Prometheus





