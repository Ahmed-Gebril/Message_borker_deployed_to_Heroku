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


def add_state(new_state,state_key='state'):
	"""Adds new application state to redis for state management.

	Args:
		new_state (str): One of the state to be added. `PAUSED`, `RUNNING`, `INIT`, `SHUTDOWN`
		state_key (str): Key to point out the stored state data
	"""
	if state_exists(state_key):

		data = get_redis_state(state_key)
	else:
		data = []

	data.append({'state':new_state,'timestamp':datetime.datetime.utcnow().isoformat()})

	redis_client.set(state_key,json.dumps(data))
	

def state_exists(state_key='state'):
	"""

	Args:
		state_key (str): Key to point out stored state data. 

	Returns:
		[Boolean]: Returns True if given state_key exits else returns false
	"""
	value = redis_client.get(state_key)
	if value:
		return True
	else:
		return False

def get_redis_state(state_key='state'):
	"""Returns all state data present in state_key.

	Args:
		state_key (str): Defaults to 'state'.
		Key to point out stored state data. 

	Returns:
		[List]: List of dicts where single dict has {'state':....,'timestamp':....}
	"""
	return json.loads(redis_client.get(state_key))

def get_current_state(state_key='state'):
	"""Returns latest state data present in the state_key.
		Returns  False if no state is set yet.

	Args:
		state_key (str): Defaults to 'state'.
		Key to point out stored state data. 

	Returns:
		[dict/boolean]: Reurns dict if state is set else a False boolean.
	"""
	if state_exists(state_key):
		data = json.loads(redis_client.get(state_key))
		return data[-1]
	else:
		return False

def remove_state(state_key='state'):
	"""Completely removes the state key and its contents.

	Args:
		state_key (str): Defaults to 'state'.
		Key to point out stored state data. 
	"""
	redis_client.delete(state_key)
	



	
if __name__ == "__main__":
	api.run()