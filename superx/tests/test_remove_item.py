'''
import client session
'''
import pytest
from flask import session


@pytest.mark.run(order=5)
def test_remove_item(client):
    test_item = {
        'id': '123123123',
        'name': 'ananas',
        'quantity': '1',
        'is_weighted': 'True',
        'unit_of_measure': 'קילו'
    }

    with client:
        client.post('/addItem', data=test_item, follow_redirects=True)
        client.post('/removeItem', data=test_item, follow_redirects=True)
        assert session['cart'] == []
