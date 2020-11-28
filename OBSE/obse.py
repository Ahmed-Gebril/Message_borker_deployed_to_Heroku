import pika
import time
import datetime
import os

TOPIC_RX = 'my.o'
TOPIC_TX = 'my.i'
EXAHANGE ='layered_topic_exchange'


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbit'))
channel = connection.channel()

channel.exchange_declare(exchange=EXAHANGE, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
        exchange=EXAHANGE, queue=queue_name, routing_key='#')



def callback(ch, method, properties, body):
    timestamp = datetime.datetime.utcnow().isoformat()
    topic = method.routing_key
    log_msg = f"""{timestamp} Topic {topic}: {body.decode()}\n"""
    print(log_msg)
    with open('/usr/data/log.txt','a') as f:
        f.write(log_msg)
    


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

#removing old entry
if os.path.exists('/usr/data/log.txt'):
	os.remove('/usr/data/log.txt')

channel.start_consuming()