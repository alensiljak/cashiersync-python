'''
'''
# import pytest

#@pytest.fixture
def test_lots():
    from cashiersync.app import app
    import json

    client = app.test_client()
    response = client.get('/lots?symbol=VYM')

    assert response is not None
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result is not None

def test_search():
    from cashiersync.app import app
    import json

    client = app.test_client()
    response = client.post('/search?symbol=VYM', 
        json = {"dateFrom":"2021-01-09","dateTo":"2021-01-17",
            'payee':None,"freeText":None})

    assert response is not None
    assert response.status_code == 200
    result = json.loads(response.data)
    assert result is not None
