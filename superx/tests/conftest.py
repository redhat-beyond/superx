'''
importing pytet and app
'''
import pytest
from app import app # pylint: disable=import-error


@pytest.fixture(scope="session", autouse=True)
def client():
    '''
    configuring pytest and test client to use
    '''
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['TESTING'] = True
    return app.test_client()


