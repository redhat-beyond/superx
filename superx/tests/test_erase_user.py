'''
import User from models and pytest and database
'''
import pytest
from app import db # pylint: disable=import-error
from models import User # pylint: disable=import-error

@pytest.mark.run(order=4)
def test_erase_user():
    '''
    tests erase the user from the database
    '''
    user = User.query.filter(User.email == 'aryehlevklein@gmail.com').first()
    User.query.filter(User.id == user.id).delete()
    db.session.commit()
    assert  User.query.filter(User.email == 'aryehlevklein@gmail.com').first() is None
