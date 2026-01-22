from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.api.auth.router import router as auth_router
from app.api.users.router import router as users_router
from app.api.organizations.router import router as org_router
from app.api.projects.router import router as projects_router
from app.api.incidents.router import router as incidents_router
from app.api.comments.router import router as comments_router
from app.api.tags.router import router as tags_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Incident Tracker API",
        version="1.0.0",
        description="Production-ready B2B SaaS backend (FastAPI, RBAC, Multi-tenant)",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # ------------------------
    # CORS
    # ------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------
    # Routers
    # ------------------------
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(users_router, prefix="/users", tags=["Users"])
    app.include_router(org_router, prefix="/organizations", tags=["Organizations"])
    app.include_router(projects_router, prefix="/organizations/{organization_id}/projects",tags=["Projects"])
    app.include_router(incidents_router, prefix="/organization/{organization_id}/projects/{project_id}/incidents", tags=["Incidents"])
    app.include_router(comments_router, prefix="/organization/{organization_id}/incident/{incident_id}/comments", tags=["Comments"])
    app.include_router(tags_router, prefix="/organizations/{organization_id}/tags", tags=["Tags"])

    return app

app = create_app()