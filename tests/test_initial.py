import requests


""" def test_check_status_code_equals_200():
  
    response = requests.get("http://172.19.0.1:8080")
    assert response.status_code == 200

 """


 @api.route('/api/state',methods=['GET'])
def get_state():
	current_state = get_current_state()

	if current_state:
		return get_current_state()['state'],200
	else:
		#returning empty response when there is no state presnet.
		return '',200