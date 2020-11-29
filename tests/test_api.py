import sys
#only 'tests' module is present in sys path for package lookup
#adding outer level to import from root  folder.
sys.path.append('..')
import apigateway
import pytest
import json


#creating a test_client fixture to test the api gateway.
@pytest.fixture
def test_client():
    flask_app = apigateway.api
    # Creating test client for FLask
    with flask_app.test_client() as test_client:
        # Pushing application context for test_client
        with flask_app.app_context():
            yield test_client

def test_get_messages_endpoint(test_client):
    """
        Checks for a 200 status code when a GET request is send over '/api/messages
    """
    response = test_client.get('/api/messages')
    assert response.status_code == 200
        
    #test for log file present
    if len(response.data) > 0:
        assert b'Topic' in response.data
    else:
        #log file isn't present. response is empty
        assert b'' == response.data

def test_put_state_endpoint(test_client):
    """
        Checks for a 200 status code when a PUT request is send over '/api/state
    """
    response = test_client.put('/api/state')
    assert response.status_code == 200

def test_get_state_endpoint(test_client):
    """
         Checks for a 200 status code when a GET request is send over '/api/state
    """
    response = test_client.get('/api/state')
    assert response.status_code == 200

def test_get_run_log_endpoint(test_client):
    """
        Checks for a 200 status code when a GET request is send over '/api/run-log
    """
    response = test_client.get('/api/run-log')
    assert response.status_code == 200

def test_get_state_endpoint(test_client):
    """
         Checks for a 200 status code when a GET request is send over '/api/state
         Also checks for state to be INIT which is set by previous test case.
    """
    response = test_client.get('/api/state')
    assert response.status_code == 200
    #if test is run before starting orig, state should be INIT set by above `test_put_state_endpoint_with_payload`
    #or state should be RUNNING if test is run after starting orig.
    assert b'INIT' in response.data or b'RUNNING' in response.data

def test_put_state_endpoint_without_payload(test_client):
    """
        Checks for a 401 status code when a PUT request is send over '/api/state without payload
    """
    response = test_client.put('/api/state')
    assert response.status_code == 401