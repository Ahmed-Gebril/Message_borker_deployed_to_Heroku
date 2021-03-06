import pika
import time

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
        exchange=EXAHANGE, queue=queue_name, routing_key=TOPIC_RX)



def callback(ch, method, properties, body):
    time.sleep(1)
    message = "Got {}".format(body.decode())
    print(message)
    channel.basic_publish(exchange=EXAHANGE, routing_key=TOPIC_TX, body=message)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()