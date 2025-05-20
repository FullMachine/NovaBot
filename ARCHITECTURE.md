# Architecture Document — Nova Sports Data Platform

## 1. System Overview
Nova Sports Data Platform is a unified, extensible system for scraping, verifying, and serving real-time and historical sports data (NBA, NFL, MLB, Esports, Golf, Tennis, etc.) to fans, analysts, and teams via a modern web dashboard and robust APIs. The system is designed for reliability, speed, and easy extensibility.

---

## 2. Component Breakdown
- **Scraper Service:** Python async jobs for each sport, modular and resumable, with error handling and logging.
- **Verification Pipeline:** Cross-checks scraped data with official APIs, flags discrepancies, and generates reports.
- **Data Store:** Centralized storage (PostgreSQL for structured data, S3-compatible object storage for raw files/CSVs).
- **API Layer:** FastAPI (Python) backend serving REST/GraphQL endpoints for all data access and admin actions.
- **Frontend Dashboard:** Next.js (React) app for users to browse, search, and interact with sports data.
- **Task Queue:** Celery (with Redis) for background jobs, retries, and scheduling.
- **Auth Service:** JWT-based authentication, with OAuth2 support for future integrations.
- **Monitoring & Logging:** Prometheus + Grafana for metrics, Sentry for error tracking.

---

## 3. Chosen Stack
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy, Celery, Redis
- **Scraping:** aiohttp, requests, BeautifulSoup4, tenacity (for retries)
- **Database:** PostgreSQL (RDS-ready), SQLAlchemy ORM
- **Object Storage:** AWS S3 or MinIO (for local/dev)
- **Frontend:** Next.js (React 18+), TypeScript, TailwindCSS, SWR/React Query
- **Testing:** pytest, pytest-asyncio, unittest.mock, Cypress (frontend)
- **DevOps:** Docker, GitHub Actions, Terraform (infra-as-code)

---

## 4. API Interfaces and Contracts
- **REST/GraphQL Endpoints:**
  - `/api/v1/players?league=NBA&season=2023-24`
  - `/api/v1/games?league=NFL&date=2024-09-01`
  - `/api/v1/verify/report?league=MLB`
  - `/api/v1/user/favorites` (POST/GET)
- **OpenAPI Spec:** All endpoints documented and auto-generated via FastAPI.
- **Frontend-Backend Contract:** TypeScript interfaces auto-generated from OpenAPI schema (e.g., using openapi-typescript).

---

## 5. Database Schema / Storage Plan
- **PostgreSQL Tables:**
  - `players` (id, name, league, team, position, stats, updated_at)
  - `games` (id, league, season, date, teams, stats, updated_at)
  - `user` (id, email, password_hash, created_at)
  - `favorites` (user_id, player_id, created_at)
  - `watchlist` (user_id, player_id, created_at)
  - `verification_reports` (id, league, report_json, created_at)
- **Object Storage:**
  - Raw CSVs, JSON dumps, and backup files stored by league/season/date

---

## 6. Data Flow Diagram (Mermaid.js)
```mermaid
flowchart TD
    subgraph Scraping
      A[Scraper Service] --> B[Verification Pipeline]
    end
    B --> C[PostgreSQL DB]
    B --> D[S3/MinIO Storage]
    C --> E[API Layer (FastAPI)]
    D --> E
    E --> F[Next.js Frontend]
    E --> G[External Consumers (API)]
    F -->|User Actions| E
    E -->|Auth| H[Auth Service]
    A -->|Logs| I[Monitoring/Logging]
    B -->|Reports| C
```

---

## 7. Authentication & Security
- **JWT-based Auth:** All API endpoints require JWT tokens; refresh tokens for session management.
- **OAuth2 Ready:** For future Google/Apple login.
- **RBAC:** Role-based access for admin/user endpoints.
- **Rate Limiting:** Per-user and per-IP limits on API endpoints (e.g., via Redis).
- **Data Validation:** Pydantic models for all input/output.
- **Secrets Management:** Use AWS Secrets Manager or environment variables (never hardcode).
- **HTTPS Everywhere:** Enforced at load balancer and app level.

---

## 8. Testing Strategy (TDD)
- **Test Philosophy:** TDD is required. All new features must start with tests (unit, integration, e2e).
- **Backend:** pytest + pytest-asyncio for all services; 90%+ coverage required for MVP.
- **Frontend:** Cypress for e2e, React Testing Library for components.
- **CI/CD:** All tests must pass before merge (GitHub Actions pipeline).
- **Mocking:** Use unittest.mock and VCR.py for external API calls.
- **Load Testing:** k6 or Locust for API endpoints.

---

## 9. Future Scalability Considerations
- **Horizontal Scaling:** All services are stateless and Dockerized; can be scaled via Kubernetes/ECS.
- **Read Replicas:** PostgreSQL read replicas for heavy analytics workloads.
- **Async Pipelines:** All scraping and verification jobs are async and queue-based.
- **API Gateway:** For rate limiting, caching, and versioning as usage grows.
- **Plugin System:** New sports or data sources can be added as plugins (clear interface contract).
- **Observability:** All logs and metrics are centralized for easy debugging and scaling.

---

## 10. Folder Structure (MVP Example)
```
/ (repo root)
  /backend
    /app
      /api
      /models
      /services
      /schemas
      /tasks
      /tests
    Dockerfile
  /scrapers
    /nba
    /nfl
    /mlb
    /esports
    /golf
    /tennis
    /common
    /tests
  /frontend
    /src
      /components
      /pages
      /lib
      /styles
      /tests
    Dockerfile
  /infra
    /terraform
    /scripts
  /docs
  README.md
  .env.example
```

---

**Trade-offs:**
- Python for scraping and backend: best async/data ecosystem, but not as fast as Go/Node for ultra-high throughput (acceptable for MVP, can optimize later).
- Next.js/React: fastest to build beautiful, interactive dashboards; easy to hire for.
- PostgreSQL: strong consistency and relational queries; can add NoSQL for unstructured data if needed.

---

**This architecture is designed for rapid MVP delivery, but every decision supports long-term scale and extensibility.** 