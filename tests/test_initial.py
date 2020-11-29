import requests

def test_check_status_code_equals_200():
     response = requests.get("http://localhost:8080")
     assert response.status_code == 200