import requests


def test_check_status_code_equals_200():
    """
       Checks for a 200 response when get request is sent to port 8080, where messages are produced.
    """
    response = requests.get("http://172.19.0.1:8080")
    assert response.status_code == 200

