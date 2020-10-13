import pytest

from app import db
from models import User

@pytest.mark.run(order=4)
def test_erase_user():
    user = User.query.filter(User.email == 'aryehlevklein@gmail.com').first()
    User.query.filter(User.id == user.id).delete()
    db.session.commit()

    assert  User.query.filter(User.email == 'aryehlevklein@gmail.com').first() == None