import pytest
from superx/routes import signup

@pytest.fixture
def user1():
    email = 'doesnotexist@down.com'
    password = 'abcd1234'
    return {email, password}

@pytest.fixture
def user2():
    email = 'doesnotexist@gmail.com'
    password = 'abcd12345'
    return {email, password}

@pytest.fixture
def user3():
    email = 'doesnotexist@down.com'
    password = 'abcd'
    return {email, password}

# Soon to be more tests
def test_register():
    validate_email(self, user3()[0])
    assert validate_email(self,user3()[0]) == error_message
    