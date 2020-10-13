import pytest
from models import User

@pytest.mark.run(order=3)
def test_logout_user(client):

    
    
    client.get('/logout', follow_redirects=True)
    user = User.query.filter(User.email == 'aryehlevklein@gmail.com').first()
    
    assert  user.is_authenticated == False
    