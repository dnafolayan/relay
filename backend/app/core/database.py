from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import AppSettings

settings = AppSettings()

engine = create_engine(settings.db_url.get_secret_value())
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
