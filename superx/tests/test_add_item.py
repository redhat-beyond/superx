'''
import session for cart
'''
import pytest
from flask import session



@pytest.mark.run(order=4)
def test_add_item(client):
    '''
    checks that item is removed from cart in flask sessions
    '''
    test_item = {
        'id': '123123123',
        'name': 'ananas'
    }
    with client:
        client.post('/addItem', data=test_item, follow_redirects=True)
        assert test_item in session['cart']
