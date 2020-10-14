import pytest
from app import app
from app import db
from models import User

@pytest.fixture
def client():
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True
    return app.test_client()

