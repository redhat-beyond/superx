'''
import client session
'''
import pytest
from flask import session


@pytest.mark.run(order=5)
def test_remove_item(client):
    '''
    tests removing item from comparing cart
    '''
    test_item_to_remove = {
        'id': '123123123'
    }

    with client:
        client.post('/removeItem', data=test_item_to_remove, follow_redirects=True)
        assert session['cart'] == []
