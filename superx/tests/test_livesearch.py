"""
import html parser
"""
import pytest
from bs4 import BeautifulSoup
from app import db
# pylint: disable=unused-import
# pylint: disable=no-else-continue


@pytest.mark.run(order=4)
def test_livesearch(client):
    """
    tests livesearch functionality
    """
    item_input1 = {'input': "שימורים"}
    item_input2 = {'input': "sdsdd"}
    item_input3 = {'input': "     "}
    item_input4 = {'input': ""}

    do_it(client, item_input1)
    do_it(client, item_input2)
    do_it(client, item_input3)
    do_it(client, item_input4)


def do_it(client, item_input):
    """
    execute the tests
    """
    with client:
        response = client.get('/livesearch', data=item_input, follow_redirects=True)
        cart_html = BeautifulSoup(response.data, 'html.parser')

        is_inside = True
        item_list = cart_html.findAll('td', {'id': True})

        if not item_list:
            is_inside = False
            assert is_inside is False
        else:
            for item in item_list:
                if item_input.get('input') in item.text:
                    continue
                else:
                    is_inside = False
                    break
            assert is_inside is True
        print(is_inside)
