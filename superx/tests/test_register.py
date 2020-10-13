from app import db
from models import User
from werkzeug.security import check_password_hash


def test_register_user(client):
    
    test_user = {
        'username': 'Admin',
        'email': 'a@gmail.com',
        'password' : '12345678',
        'submit': 'צור משתמש חדש'
    }
    # Register new user
    client.post('/register', data=test_user, follow_redirects=True)

    validate_user = User.query.filter(User.email == 'a@gmail.com').first()
    assert validate_user.name == 'Admin'
    assert validate_user.email == 'a@gmail.com'
    assert validate_user.password == check_password_hash(validate_user.password, '12345678')
    User.query.filter(User.id == validate_user.id).delete()
    db.session.commit()
    User.query.filter(User.id == validate_user.id).delete()
    db.session.commit()
