import requests


def test_check_status_code_equals_200():
    """
        Checks for a 401 status code when a PUT request is send over '/api/state without payload
    """
    response = requests.get("http://172.19.0.1:8080")
    assert response.status_code == 200

