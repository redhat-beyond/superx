'''
import session for cart
'''
import pytest
from flask import session



@pytest.mark.run(order=5)
def test_add_item(client):
    '''
    checks that item is added to cart in flask sessions
    '''
    test_item_id = {
        'id': '123123123',
    }

    test_item = {
        'id': '123123123',
        'name': 'ananas'
    }

    with client:
        client.post('/addItem', data=test_item_id, follow_redirects=True)
        assert test_item not in session['cart']
