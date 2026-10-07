from fastapi import FastAPI

from .core.config import AppSettings

settings = AppSettings()  # app settings
app = FastAPI(title=settings.app_name, description=settings.app_description)


@app.get("/health")
def health_check():
    return {"status": "ok"}
