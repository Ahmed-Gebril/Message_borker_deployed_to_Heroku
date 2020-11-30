import requests


def test_check_status_code_equals_200():
  
    response = requests.get("http://172.19.0.1:8080")
    assert response.status_code == 200

