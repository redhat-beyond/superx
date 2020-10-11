from app import db
from models import User
from werkzeug.security import check_password_hash, generate_password_hash


def test_register_user(client):
    
    test_user = {
        'username': 'Admin',
        'email': 'aryehlevklein@gmail.com',
        'password' : '12345678',
    }
    # Register new user
    client.post('/register', data=test_user, follow_redirects=True)

    validate_user = User.query.filter(User.email == 'aryehlevklein@gmail.com').first()
    assert validate_user.name == 'Admin'
    assert validate_user.email == 'aryehlevklein@gmail.com'
    # assert validate_user.password == check_password_hash(validate_user.password, generate_password_hash('12345678', method='sha256'))
    User.query.filter(User.id == validate_user.id).delete()
    db.session.commit()
    User.query.filter(User.id == validate_user.id).delete()
    db.session.commit()
