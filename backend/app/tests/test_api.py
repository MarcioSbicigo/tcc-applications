from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def setup_database():
    # Mockando a função que interage com o MongoDB
    with patch('app.routers.register') as mock_create_user:
        # Configurando o mock para retornar um valor quando chamado
        mock_create_user.return_value = {"username": "testuser"}
        
        # Executar testes
        yield mock_create_user

def test_register_user(setup_database):
    response = client.post("/api/v1/register", json={
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "User successfully registered: testuser"}
    
    # Verificando se a função de criar usuário foi chamada
    setup_database.assert_called_once_with(
        username="testuser",
        full_name="Test User",
        email="test@example.com",
        password="password123"
    )

def test_login_user(setup_database):
    response = client.post("/api/v1/login", json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "token" in response.json()
