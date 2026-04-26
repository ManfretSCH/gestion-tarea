import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db, base

# 1. Engine de SQLite en memoria (solo para tests)
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine_test = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False}  # necesario para SQLite
)

# 2. Fábrica de sesiones para los tests
TestingSession = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_test
)

# 3. Fixture que prepara y limpia la DB en cada test
@pytest.fixture
def client():
    # Creá las tablas en SQLite
    base.metadata.create_all(bind=engine_test)

    # Función que reemplaza a get_db durante el test
    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    # Instalá el override ANTES de crear el TestClient
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c  # acá corre el test

    # Limpieza: eliminá tablas y remové el override
    base.metadata.drop_all(bind=engine_test)
    app.dependency_overrides.clear()