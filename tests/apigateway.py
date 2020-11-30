from flask import Flask,request,jsonify
import os
import requests
import redis
import json
import datetime
import time
api = Flask(__name__)
redis_client =  redis.Redis(host='172.19.0.1', port=6379, decode_responses=True)

@api.route('/api/messages',methods=['GET'])
def get_messages():
	response = requests.get('http://172.19.0.1:8080')
	return response.content,response.status_code,response.headers.items()

@api.route('/api/state',methods=['PUT'])
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

@api.route('/api/node-statistic',methods=['GET'])
def get_node_statistic():
	NODE_API = 'http://172.19.0.1:15672/api/nodes'
	json_response = requests.get(NODE_API,auth=('guest','guest')).json()[0]
	return jsonify({
		'disk_free':json_response.get('disk_free',None),
		'fd_used':json_response.get('fd_used',None),
		'os_pid':json_response.get('os_pid',None),
		'uptime':json_response.get('uptime',None),
		'node_type':json_response.get('type',None),
	})
@api.route('/api/queue-statistic',methods=['GET'])
def get_queue_statistic():
	QUEUE_API = 'http://172.19.0.1:15672/api/queues?msg_rates_age=3600'
	QUEUE_MESSAGE_API = 'http://172.19.0.1:15672/api/queues/%2F/{}/get'

	delivered_message_payload = json.dumps({"count":-1,"ackmode":"ack_requeue_false","encoding":"auto","truncate":50000})
	published_message_payload = json.dumps({"count":100000,"ackmode":"ack_requeue_true","encoding":"auto","truncate":50000})

	all_queues = requests.get(QUEUE_API,auth=('guest','guest')).json()
	
	response_data = []
	for single_queue in all_queues:
		queue_name = single_queue['name']

		delivered_message_data = requests.post(QUEUE_MESSAGE_API.format(queue_name),auth=('guest','guest'),data=delivered_message_payload).json()
		published_message_data = requests.post(QUEUE_MESSAGE_API.format(queue_name),auth=('guest','guest'),data=published_message_payload).json()

		if delivered_message_data:
			delivered_message = delivered_message_data[-1]['payload']
		else:
			delivered_message = None
		
		if published_message_data:
			published_message = published_message_data[-1]['payload']
		else:
			published_message = None

		response_data.append({
			'queue_name':queue_name,
			'message_delivery_rate':single_queue['message_stats']['deliver_no_ack_details']['rate'],
			'message_publish_rate':single_queue['message_stats']['publish_details']['rate'],
			'delivered_message':delivered_message,
			'published_message':published_message,
		})
		#control req/sec to prevent server overload 500 error
		time.sleep(3)
	return jsonify(response_data)

def add_state(new_state,state_key='state'):
	"""Adds new application state to redis for state management.

	Args:
		new_state (str): One of the state to be added. `PAUSED`, `RUNNING`, `INIT`, `SHUTDOWN`
		state_key (str): Key to point out the stored state data
	"""
	if state_exists(state_key):

		data = get_redis_state(state_key)
		current_state = get_current_state(state_key)['state']
	else:
		data = []
		current_state = ''
	#if new state is different from current state then only state is updated.
	if current_state != new_state:
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
