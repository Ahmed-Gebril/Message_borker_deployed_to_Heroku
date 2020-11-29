from flask import Flask,request,jsonify
import os
import requests
import redis
import json
import datetime
import time
api = Flask(__name__)
redis_client =  redis.Redis()

@api.route('/api/messages',methods=['GET'])
def get_messages():
	response = requests.get('http://host.docker.internal:8080/')
	return response.content,response.status_code,response.headers.items()

def put_state():
	payload = request.get_json() or request.form.to_dict()
	#payload validation
	if not payload:
		return '',400

	add_state(payload['state'])
	return '',200

@api.route('/api/state',methods=['GET'])
def get_state():
	current_state = get_current_state()

	if current_state:
		return get_current_state()['state'],200
	else:
		#returning empty response when there is no state presnet.
		return '',200

@api.route('/api/run-log',methods=['GET'])
def get_run_log():
	if not state_exists():
		return '',200
	data = get_redis_state()
	formatted_data = [i['timestamp']+': '+i['state'] for i in data]
	return '\n'.join(formatted_data)





	
if __name__ == "__main__":
	api.run()