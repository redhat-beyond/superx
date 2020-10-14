from app import db
from models import User
from werkzeug.security import  generate_password_hash
from flask import url_for, request
import pytest

@pytest.mark.run(order=2)
def test_login_user(client):
    
    fake_user = {
        'email': 'fake@fake.com',
        'password' : '12345678',
    }
    response = client.post('/login', data=fake_user, follow_redirects=True)
    assert b'*Email does not exist*' in response.data
    
    hash_password = generate_password_hash('12345678', method='sha256')
    
    test_user = {
        'email': 'aryehlevklein@gmail.com',
        'password' : '12345678',
    }
    user = User.query.filter(User.email == 'aryehlevklein@gmail.com').first()
    
    
    client.post('/login', data=test_user, follow_redirects=True)
    
    assert user.is_authenticated == True


    