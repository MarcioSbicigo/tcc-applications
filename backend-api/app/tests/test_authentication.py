import pytest
from fastapi.testclient import TestClient
from dependencies import database_requests
from fastapi import FastAPI
from fastapi import FastAPI
from routers.v1 import login, logout, register

app = FastAPI()

# Incluindo as Rotas
app.include_router(login.router)
app.include_router(register.router)
app.include_router(logout.router)

@app.get('/')
def inicializacao() -> str:
    return 'API em execução...'

client = TestClient(app)

@pytest.fixture(autouse=True)
def set_env_variables(monkeypatch):
    # Defina as variáveis de ambiente necessárias antes de executar os testes
    monkeypatch.setenv('MONGO_URI', 'mongodb://localhost:27017')
    monkeypatch.setenv('REDIS_URI', 'redis://localhost:6379')

def test_register_user():
    response = client.post("/api/v1/register", json={
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@user.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "User successfully registered: testuser"}

    # Verificar se o usuário foi realmente inserido no banco de dados
    users_collection = database_requests.get_users_collection()
    user = users_collection.find_one({"username": "testuser"})
    assert user is not None

def test_login_user():
    response = client.post("/api/v1/login", json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()