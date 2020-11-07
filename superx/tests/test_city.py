'''
import User from models and pytest and database
'''
import pytest
from flask import session 


@pytest.mark.run(order=7)
def test_choose_city(client):
    '''
    tests add city
    '''
    test_city = {
        'city' : 'ירושלים'
    }
    with client:
        client.post('/city', data=test_city, follow_redirects=True)
        assert session['city'] is 'ירושלים'
 