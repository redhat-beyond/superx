"""
import html parser
"""
import pytest
from bs4 import BeautifulSoup


@pytest.mark.run(order=6)
def test_livesearch(client):
    """
    tests livesearch functionality
    """
    item_input1 = {'input': "שימורים"}
    item_input2 = {'input': "sdsdd"}
    item_input3 = {'input': "     "}
    item_input4 = {'input': ""}

    city_input = {'city': 'ירושלים'}

    execute_test(client, item_input1, city_input)
    execute_test(client, item_input2, city_input)
    execute_test(client, item_input3, city_input)
    execute_test(client, item_input4, city_input)


def execute_test(client, item_input, city_input):
    """
    execute the tests
    """
    with client:
        client.get('/city', data=city_input, follow_redirects=False)
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
                is_inside = False
                break
            assert is_inside
