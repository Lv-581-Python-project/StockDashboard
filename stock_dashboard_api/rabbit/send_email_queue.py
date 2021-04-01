import pika


def connect_queue():
    rabbitmq = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    return rabbitmq


def get_email_queue():
    connect = connect_queue()
    channel = connect.channel()
    channel.queue_declare(queue='email_queue', durable=True)
    channel.queue_bind(exchange='amq.direct', queue='email_queue')
    email_queue = channel
    return email_queue
