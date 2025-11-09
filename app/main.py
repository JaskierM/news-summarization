from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv
from sber_isutop_toolbox.fastapi import handle_exceptions
from sber_isutop_toolbox.fastapi.swagger import ISUSwagger

from app.api.v1.chat import chat_router
from app.core.settings.app import load_settings
from app.core.utils.logging import logger

_app_settings = load_settings()


def create_app() -> FastAPI:
    load_dotenv(find_dotenv(usecwd=True))

    logger.info("Starting application...")

    app = FastAPI(
        title=_app_settings.PROJECT_NAME,
        version=_app_settings.VERSION,
        openapi_url=f"{_app_settings.BASE_PREFIX}/openapi.json",
        docs_url=f"{_app_settings.BASE_PREFIX}/docs" if _app_settings.DOCS else None,
        redoc_url=f"{_app_settings.BASE_PREFIX}/redoc" if _app_settings.DOCS else None,
    )
    logger.info("Created FastAPI app")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_app_settings.CORS_ORIGINS,
        allow_credentials=_app_settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=_app_settings.CORS_ALLOW_METHODS,
        allow_headers=_app_settings.CORS_ALLOW_HEADERS,
    )

    root = APIRouter(prefix=_app_settings.BASE_PREFIX)
    logger.info("Created root router")

    @root.get("/health", tags=["infra"])
    async def health() -> dict:
        return {"status": "ok", "env": _app_settings.ENV.value}

    root.include_router(chat_router)
    app.include_router(root)
    logger.info("Included all routers")

    app.add_exception_handler(Exception, handle_exceptions)
    logger.register_fastapi(app)
    ISUSwagger().register_fastapi(app)
    logger.info("Registered: exception handler, logger and swagger")

    return app


app = create_app()
