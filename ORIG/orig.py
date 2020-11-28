import pika
import time
from threading import Event

TOPIC_TX = 'my.o'
EXAHANGE ='layered_topic_exchange'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
channel = connection.channel()

channel.exchange_declare(exchange=EXAHANGE,exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
        exchange=EXAHANGE, queue=queue_name, routing_key=TOPIC_TX)

def send_message():
    for i in range(1,4):
        message = 'MSG_{}'.format(i)
        print(message)
        channel.basic_publish(exchange=EXAHANGE, routing_key=TOPIC_TX, body=message)
        
        if i!=3:
            time.sleep(3)

if __name__ == "__main__":
    send_message()
    #closing connection channel after message publish.
    channel.close()
    #blocking exit to prevent container restarted after program exit.
    Event().wait()



