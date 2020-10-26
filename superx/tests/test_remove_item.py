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
    test_item = {
        'id': '45232123',
        'name': 'mushrooms',
        'quantity': '2',
        'is_weighted': 'Flase',
        'unit_of_measure': 'גרם'
    }
    
    oldcart = session['cart'].copy() 
    
    with client:
        client.post('/addItem', data=test_item, follow_redirects=True)
        client.post('/removeItem', data=test_item, follow_redirects=True)
        assert session['cart'] == oldcart
