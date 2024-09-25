# import pytest
# from app.dash_app import app

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# def test_login_page(client):
#     response = client.get('/login')
#     assert response.status_code == 200
#     assert b"Login" in response.data

# def test_register_page(client):
#     response = client.get('/register')
#     assert response.status_code == 200
#     assert b"Register" in response.data


# import unittest
# from unittest.mock import patch
# from app import app  # Supondo que o arquivo do app se chama 'app.py'

# class TestLogin(unittest.TestCase):

#     def setUp(self):
#         self.app = app.test_client()
#         self.app.testing = True

#     @patch('app.find_user_in_database')  # Mockando a função que acessa o banco de dados
#     def test_login_success(self, mock_find_user):
#         # Simulando um usuário encontrado no banco
#         mock_find_user.return_value = {"username": "testuser", "password": "hashed_password"}

#         # Simulando o POST para a rota de login
#         response = self.app.post('/login', json={
#             'username': 'testuser',
#             'password': 'correct_password'
#         })

#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Login successful", response.data)

#     @patch('app.find_user_in_database')
#     def test_login_invalid_credentials(self, mock_find_user):
#         # Simulando usuário não encontrado
#         mock_find_user.return_value = None

#         response = self.app.post('/login', json={
#             'username': 'invaliduser',
#             'password': 'wrong_password'
#         })

#         self.assertEqual(response.status_code, 400)
#         self.assertIn(b"Invalid credentials", response.data)

# if __name__ == '__main__':
#     unittest.main()


from unittest.mock import patch
import pytest

# Supondo que `login_request` seja importado do seu módulo
from app.dash_app import login_request

@pytest.fixture
def mock_login_success():
    with patch('app.components.api.my_budget_api.LoginRequest') as mock:
        mock.return_value = 'fake_token'  # Simula um token válido
        yield mock

@pytest.fixture
def mock_login_failure():
    with patch('app.components.api.my_budget_api.LoginRequest') as mock:
        mock.side_effect = Exception("Invalid credentials")  # Simula falha na autenticação
        yield mock

def test_login_success(mock_login_success):
    # Aqui você pode simular a interação com seu layout
    response = login_request(1, "valid_user", "valid_password")
    assert response['login_status'] == 'success'
    assert response['token'] == 'fake_token'

def test_login_failure(mock_login_failure):
    response = login_request(1, "invalid_user", "invalid_password")
    assert response['login_status'] == 'error'
    assert response['message'] == 'Nome de usuário e/ou senha invalido(s)'
