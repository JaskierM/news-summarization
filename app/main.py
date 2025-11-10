from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv

from app.api.v1.summarize import summarize_router
from app.core.settings.app import load_settings

_app_settings = load_settings()


def create_app() -> FastAPI:
    load_dotenv(find_dotenv(usecwd=True))

    app = FastAPI(
        title=_app_settings.PROJECT_NAME,
        version=_app_settings.VERSION,
        openapi_url=f"{_app_settings.BASE_PREFIX}/openapi.json",
        docs_url=f"{_app_settings.BASE_PREFIX}/docs" if _app_settings.DOCS else None,
        redoc_url=f"{_app_settings.BASE_PREFIX}/redoc" if _app_settings.DOCS else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_app_settings.CORS_ORIGINS,
        allow_credentials=_app_settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=_app_settings.CORS_ALLOW_METHODS,
        allow_headers=_app_settings.CORS_ALLOW_HEADERS,
    )

    root = APIRouter(prefix=_app_settings.BASE_PREFIX)

    @root.get("/health", tags=["infra"])
    async def health() -> dict:
        return {"status": "ok", "env": _app_settings.ENV.value}

    root.include_router(summarize_router)
    app.include_router(root)

    return app


app = create_app()
