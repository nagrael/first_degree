import _thread
import pika


print("STARTING ADMIN")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

channel.exchange_declare(exchange='check',
                         type='topic')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, (body)))




channel.queue_bind(exchange='check',
                       queue=queue_name,
                       routing_key="personel.#")
channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)


def infloop():

    while(True):
        message = input("Write info...\n")
        if message == "exit":
            break
        channel.basic_publish(exchange='check',
                      routing_key="info",
                      body=message)

        print(" [x] Sent %r:" % ( message))



_thread.start_new_thread(infloop,())

channel.start_consuming()