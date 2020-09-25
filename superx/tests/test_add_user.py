from models import *
from app import app
from werkzeug.security import generate_password_hash


def test_add_user():
    app.config['TESTING'] = True
    hash_password = generate_password_hash('dosntmatter', method='sha256')
    test_user = User(name='admin', email='admin@example.com', password=hash_password)
    db.session.add(test_user)
    db.session.commit()
    validate_user = User.query.get(test_user.id)
    assert validate_user.name == 'admin'
    assert validate_user.email == 'admin@example.com'
    User.query.filter(User.id == validate_user.id).delete()

