"""
Database Settings
"""

from config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = get_settings().sqlalchemy_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# DBのセッションを管理
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    DB DIの設定
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()
