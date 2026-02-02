from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, auth, documents, queries, users
from app.core.config import settings
from app.db.session import init_db


app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


app.include_router(auth.router, prefix=settings.api_prefix, tags=["auth"])
app.include_router(users.router, prefix=settings.api_prefix, tags=["users"])
app.include_router(documents.router, prefix=settings.api_prefix, tags=["documents"])
app.include_router(queries.router, prefix=settings.api_prefix, tags=["queries"])
app.include_router(analytics.router, prefix=settings.api_prefix, tags=["analytics"])
