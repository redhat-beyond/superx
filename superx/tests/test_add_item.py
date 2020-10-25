'''
import client session
'''
#pylint: disable=missing-function-docstring
import pytest
from flask import session


@pytest.mark.run(order=4)
def test_add_item(client):
    '''
    tests adding item to comparing cart
    '''
    test_item = {
        'id': '123123123',
        'name': 'ananas',
        'quantity': '1',
        'is_weighted': 'True',
        'unit_of_measure': 'קילו'
    }

    with client:
        client.post('/addItem', data=test_item, follow_redirects=True)
        item = session['cart'][-1]
        assert item["id"] == test_item["id"]
        assert item["name"] == test_item["name"]
