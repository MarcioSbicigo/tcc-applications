from dash import Dash, html
import pytest
from dash.testing.application_runners import import_app

@pytest.fixture
def app():
    app = import_app('app.dash_app')  # Supondo que sua aplicação Dash está em main.py
    yield app

def test_login_layout(app):
    with app.test_client() as client:
        response = client.get('/')
        assert b'Login' in response.data
        assert b'Username' in response.data
        assert b'Password' in response.data
