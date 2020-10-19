'''
import User from models and pytest
'''
import pytest
from models import User # pylint: disable=import-error


@pytest.mark.run(order=2)
def test_login_user(client):
    '''
    tests login the user that was registered in last test to the database
    '''
    fake_user = {
        'email': 'fake@fake.com',
        'password' : '12345678',
    }
    response = client.post('/login', data=fake_user, follow_redirects=True)
    assert b'*Email does not exist*' in response.data
    test_user = {
        'email': 'aryehlevklein@gmail.com',
        'password' : '12345678',
    }
    user = User.query.filter(User.email == 'aryehlevklein@gmail.com').first()
    client.post('/login', data=test_user, follow_redirects=True)
    assert user.is_authenticated is True
