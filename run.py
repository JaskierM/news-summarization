import uvicorn

from app.core.settings.app import load_settings

_app_settings = load_settings()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=_app_settings.HOST,
        port=_app_settings.PORT,
        reload=_app_settings.RELOAD,
    )
