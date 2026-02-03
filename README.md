# Movie API — Overview

This repository implements a movie API and related infrastructure components. The repo uses a multi-branch structure where each branch encapsulates a focused area of the project (backend, frontend/gateway, deployment, observability, infra, images, etc.). This README serves as the canonical entry point for developers and operators.

Last updated: 2026-02-03
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
This repository contains a RESTful Movie API service along with infrastructure-as-code, observability and deployment tooling. The repo is organized as a collection of branches that focus development and documentation on a single concern per branch (for example, `deployment/kubernetes` holds k8s cluster configuration, `infa/terraform` has terraform modules, etc.) and then merged on the main branch, were is the final version of the project.

Branch layout and purpose
(Branches discovered in the repository — use these names to find branch-specific content or artifacts developed)
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
  - Container images built and stored in ECR 
  - Deployable to Kubernetes with Docker builds in deployment/dockerize
  - Terraform to provision infra
- Observability & logging:
  - Metrics via Prometheus 
  - Alerts via Alertmanager 
  - Centralized logging with Logstash/Elasticsearch 

Features
- RESTful API: CRUD operations for movies
- Filtering and matrix-based search 
- Pagination and sorting
- Logging, metrics, and alerting built into infra branches
- Containerized builds and K8s manifests for production-grade deployments

Quick start

Prerequisites
- Node.js (or runtime depending on backend implementation)
- Docker (if using containers)
- kubectl 
- Terraform (if deploying infra from repo)
- A database: Postgres and/or Redis (local or remote)

Local development
1. Clone the repository:
   ```bash
   git clone https://github.com/pokerface03/movie-api.git
   cd movie-api
   ```
2. Create a virtual invironment and Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set up postgreSQL and redis
   
6. Configure environment variables (see below).
   
7. Run application locally:
   ```bash
   uvicorn controller:app --host 0.0.0.0 --port 8000
   ```
8. Access application through frontend(see script.js on branch database/redis)

Docker
- Build the image:
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
Create a `.env` with the variables the service expects.
```
PORT=3000
NODE_ENV=development
DATABASE_URL=postgres://user:pass@localhost:5432/movie_api
REDIS_URL=redis://localhost:6379
JWT_SECRET=change_this
LOG_LEVEL=info
```

Databases and caching
- PostgreSQL: initialization script in `databases/init`
- Redis: caching implementation on `backend/controller.py`

Observability and logging
- Prometheus configs and alert rules: `/Prometheus`
- Alertmanager config: `/alertmanager`
- Centralized logging and pipelines: `/filebeat`

CI/CD and images
- CI/CD definitions (pipelines) and images creation live in the .github workflows

Branch-specific notes
- Many branch READMEs are placeholders. Use this consolidated README as the main reference;






