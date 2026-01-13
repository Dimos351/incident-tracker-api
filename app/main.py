from fastapi import FastAPI
from app.api.auth.router import router as auth_router
from app.api.incidents.router import router as incidents_router
from app.api.comments.router import router as comments_router

app = FastAPI(
    title="Incident Tracker API",
    version="1.0.0",
    description="Production-ready B2B SaaS backend (FastAPI, RBAC, Multi-tenant)",
    docs_url="/docs",
    redoc_url="/redoc",
)