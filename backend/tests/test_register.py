import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API em execução..."}

@pytest.mark.asyncio
async def test_register_success():
    # Simula o banco de dados e o comportamento esperado
    with patch("dependencies.database_requests.get_users_collection") as mock_users:
        mock_users().find_one.return_value = None  # Simula que o usuário não existe

        request_data = {
            "username": "new_user",
            "full_name": "New User",
            "email": "new_user@example.com",
            "password": "password123"
        }

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/v1/register", json=request_data)

        assert response.status_code == 200
        assert response.json()["message"] == "User successfully registered: new_user"

@pytest.mark.asyncio
async def test_register_username_exists():
    # Simula que o nome de usuário já existe
    with patch("dependencies.database_requests.get_users_collection") as mock_users:
        mock_users().find_one.side_effect = [{"username": "existing_user"}, None]

        request_data = {
            "username": "existing_user",
            "full_name": "Existing User",
            "email": "existing_user@example.com",
            "password": "password123"
        }

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/v1/register", json=request_data)

        assert response.status_code == 400
        assert response.json()["detail"] == "Username already exist."

@pytest.mark.asyncio
async def test_register_email_exists():
    # Simula que o e-mail já existe
    with patch("dependencies.database_requests.get_users_collection") as mock_users:
        mock_users().find_one.side_effect = [None, {"email": "existing_email@example.com"}]

        request_data = {
            "username": "new_user",
            "full_name": "New User",
            "email": "existing_email@example.com",
            "password": "password123"
        }

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/v1/register", json=request_data)

        assert response.status_code == 400
        assert response.json()["detail"] == "E-mail already exist."

@pytest.mark.asyncio
async def test_register_database_not_exist():
    # Simula falha ao acessar o banco de dados
    with patch("dependencies.database_requests.get_database_connection") as mock_db:
        mock_db.return_value = None  # Simula que o banco de dados não existe

        request_data = {
            "username": "new_user",
            "full_name": "New User",
            "email": "new_user@example.com",
            "password": "password123"
        }

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/api/v1/register", json=request_data)

        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server error"
