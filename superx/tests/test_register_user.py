'''
import User from models and pytest
'''
from werkzeug.security import check_password_hash
import pytest
from models import User # pylint: disable=import-error


@pytest.mark.run(order=1)
def test_register_user(client):
    '''
    tests registering a user to the database
    '''
    test_user = {
        'username': 'AryehTest',
        'email': 'aryehlevklein@gmail.com',
        'password' : '12345678',
        'confirm' : '12345678',
        'city' : 'ירושלים'
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
        'city' : 'ירושלים'
    }

    add_fake_user = client.post('/register', data=fake_user, follow_redirects=True)
    assert b"*Please enter a valid email address*" in add_fake_user.data
