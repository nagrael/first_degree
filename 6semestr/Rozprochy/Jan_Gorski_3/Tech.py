import random

import pika
import sys
print("STARTING TECH")
NORM = "personel."
checks = ['knee', 'elbow', 'ankle']

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [knee/elbow/ankle] \n" % sys.argv[0])
    sys.exit(1)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='check',
                         type='topic')

result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

binding_keys = severities

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, eval(body)))
    tmp = eval(body)
    #channel.queue_declare(queue=tmp[1])
    channel.basic_publish(exchange='check',
                          routing_key=NORM+tmp[1],
                          body=tmp[0] + ": " + method.routing_key + ": badanie")
def callback_info(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

for binding_key in binding_keys:
    channel.queue_declare(queue=binding_key)
    channel.queue_bind(exchange='check',
                       queue=binding_key,
                       routing_key=NORM+binding_key)
    channel.basic_consume(callback,
                          queue=binding_key,
                          no_ack=True)
channel.queue_bind(exchange='check',
                       queue=queue_name,
                       routing_key="info")
channel.basic_consume(callback_info,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()