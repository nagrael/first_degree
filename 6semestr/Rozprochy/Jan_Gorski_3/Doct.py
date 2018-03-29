import random
import _thread
import pika
import time
print("STARTING DOCTOR")
NORM = "personel."

def callback(ch, method, properties, body):
    print(" [x] %r" %  (body))


checks = ['knee', 'elbow', 'ankle']
patinets = ['Nowak', "Adam", "Tom", "Marek", "John"]


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()



channel.exchange_declare(exchange='check',
                         type='topic')
result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue
result = channel.queue_declare(exclusive=True)

queue_name2 = result.method.queue
channel.queue_bind(exchange='check',
                   queue=queue_name,
                   routing_key=NORM+queue_name)
channel.queue_bind(exchange='check',
                   queue=queue_name2,
                   routing_key="info")
def infloop():

    while(True):
        routing_key = random.choice(checks)
        message = "[\'" + random.choice(patinets) + "\',\'" + queue_name + "\']"
        channel.basic_publish(exchange='check',
                      routing_key=NORM+routing_key,
                      body=message)
        time.sleep(1)
        print(" [x] Sent %r:%r" % (NORM+routing_key, message))

channel.basic_consume(callback,
                      queue=queue_name)
channel.basic_consume(callback,
                      queue=queue_name2)

_thread.start_new_thread(infloop,())
channel.start_consuming()
connection.close()