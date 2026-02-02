# DocQuery

DocQuery is a modern AI Knowledge Assistant built with a RAG-first architecture. It enables teams to centralize documents, apply role-based access control, and deliver citation-backed answers from trusted internal sources.

![Overview diagram](https://raw.githubusercontent.com/Sohitha-Kommineni/DocQuery---AI-Knowledge-Assistant/50547ed31937fb39e4881e74ed37c429549aa8f8/Overview.png)

## Highlights
- RAG pipeline with chunking, embeddings, and pgvector search
- Role-based access control (Admin, Manager, Employee)
- Citation-backed answers and query analytics
- Secure document ingestion with optional S3 storage
- Enterprise-grade UI for dashboard, documents, chat, and analytics

## Tech Stack
- Backend: FastAPI, SQLAlchemy, PostgreSQL + pgvector
- Frontend: React + Tailwind (Vite)
- Auth: JWT
- Storage: AWS S3 (optional, with local fallback)
- Deployment: Docker (ECS/EC2 ready)

## Project Structure
- `backend/` FastAPI API, RAG pipeline, ingestion, RBAC
- `frontend/` React dashboard with Docs, Chat, Analytics
- `docker-compose.yml` local dev stack

## Quick Start (Local)
1. Copy env templates:
   - `backend/env.example` -> `backend/.env`
   - `frontend/env.example` -> `frontend/.env`
2. Start services:
   - `docker compose up --build`
3. Open:
   - UI: `http://localhost:5173`
   - API: `http://localhost:8000` (health: `/health`)

## Authentication
Default admin user:
- Username: `admin`
- Password: `admin123`

## RAG Flow (High Level)
1. Upload document
2. Extract text → chunk → embed
3. Store embeddings in PostgreSQL (pgvector)
4. Query → embed → vector search
5. Filter by RBAC → generate answer with citations

If no relevant context is found, the assistant responds with “I don’t know.”

## Configuration
Backend config is in `backend/.env`. Key settings:
- `POSTGRES_DSN` database connection
- `OPENAI_API_KEY` for LLM + embeddings
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` for S3
- `LOCAL_STORAGE_PATH` local upload fallback (default: `local_uploads`)

Frontend config is in `frontend/.env`:
- `VITE_API_BASE_URL` (default: `http://localhost:8000/api`)

## Local Storage Fallback
If S3 credentials are not set, uploaded files are saved locally under `backend/local_uploads/`.

## Common Commands
- Start: `docker compose up --build`
- Stop: `docker compose down`
- Logs: `docker compose logs -f backend`

## Roadmap Ideas
- SSO (SAML/OIDC)
- Multi-tenant orgs and workspace-level RBAC
- Advanced analytics and feedback loops
- Scheduled ingestion and connectors (Confluence, GDrive, SharePoint)

## License
MIT
