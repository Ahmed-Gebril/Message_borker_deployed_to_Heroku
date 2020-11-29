import requests

def test_check_status_code_equals_200():

      """
        Checks for a 200 status code when a get request is sent to 
        port 8080. Where messages are produced.
      """
     response = requests.get("http://localhost:8080")
     assert response.status_code == 200