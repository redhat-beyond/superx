import pytest
from models import User

@pytest.mark.run(order=1)
def test_register_user(client):
    
    test_user = {
        'username': 'AryehTest',
        'email': 'aryehlevklein@gmail.com',
        'password' : '12345678',
        'confirm' : '12345678'
    }
    
    client.post('/register', data=test_user, follow_redirects=True)

    validate_user = User.query.filter(User.email == 'aryehlevklein@gmail.com').first()
    assert validate_user.name == 'AryehTest'
    assert validate_user.email == 'aryehlevklein@gmail.com'
    assert check_password_hash(validate_user.password, '12345678')
    
    add_existing_user = client.post('/register', data=test_user, follow_redirects=True)
    assert b"*Email already exists*" in add_existing_user.data
    fake_user = {
        'username': 'AryehTest',
        'email': 'fake_email@fake_email',
        'password' : '12345678',
        'confirm' : '12345678'
    }

    add_fake_user = client.post('/register', data=fake_user, follow_redirects=True)
    assert b"*Please enter a valid email address*" in add_fake_user.data

