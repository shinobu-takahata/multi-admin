"""
pytestの特別な役割を持つ
他のtestファイルから自動でインポートされる
"""

import os
import sys

app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(app_dir)
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker
from cruds.auth import get_current_user
from database import get_db
from models.models import Base, Item
from schemas.userschema import DecodedToken
from main import app


@pytest.fixture()
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        item1 = Item(
            name="item1", price=100, description="item1 description", user_id="1"
        )
        item2 = Item(
            name="item2", price=200, description="item2 description", user_id="2"
        )

        db.add(item1)
        db.add(item2)
        db.commit()
        yield db
    finally:
        db.close()


@pytest.fixture
def user_fixture():
    return DecodedToken(user_id=1, username="user1")


@pytest.fixture
def client_fixture(session_fixture: Session, user_fixture: DecodedToken):
    def override_get_db():
        return session_fixture

    def override_get_current_user():
        return user_fixture

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
