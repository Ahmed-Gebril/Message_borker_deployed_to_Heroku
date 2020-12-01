import pika
import time
import redis
import json
import datetime
import subprocess

TOPIC_TX = 'my.o'
EXAHANGE ='layered_topic_exchange'

redis_client =  redis.Redis(host='host.docker.internal', port=6379, decode_responses=True)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
channel = connection.channel()

channel.exchange_declare(exchange=EXAHANGE,exchange_type='topic')

result = channel.queue_declare('')
queue_name = result.method.queue

channel.queue_bind(
        exchange=EXAHANGE, queue=queue_name, routing_key=TOPIC_TX)

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

def send_message():
    count = 1
    while True:
        if not state_exists():
            #if no state is present INIT state is set.
            add_state('INIT')
            continue
        else:
            current_state = get_current_state()['state'] 
            if current_state == 'INIT':
                #state is updated from INIT to RUNNING and message is sent.
                add_state('RUNNING')
                message = 'MSG_{}'.format(count)
                print(message)
                channel.basic_publish(exchange=EXAHANGE, routing_key=TOPIC_TX, body=message)
                count += 1 
            elif current_state == 'RUNNING':
                message = 'MSG_{}'.format(count)
                print(message)
                channel.basic_publish(exchange=EXAHANGE, routing_key=TOPIC_TX, body=message)
                count += 1 
            elif current_state == 'PAUSED':
                #continue to listen for state change
                continue
            else:
				#exit app if state is other than INIT,RUNING or PAUSED, in other words 'STOP' a docker-compose command is run.
				with open("/tmp/output.log", "a") as output:
					subprocess.call("docker-compose down", shell=True, stdout=output, stderr=output)

                
         
        #for message flood control
        time.sleep(3)

if __name__ == "__main__":
    send_message()
    #closing connection channel after message publish.
    channel.close()
