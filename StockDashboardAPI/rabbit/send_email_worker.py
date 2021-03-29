import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pika
from flask import render_template

from StockDashboardAPI import app

import os


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue', durable=True)


def send_email_message(ch, method, properties, body):
    body = body.decode('utf-8')
    body = body.split(' ')

    sender = body[0]
    recipient = body[1]
    link = 'http://127.0.0.1:5000/' + body[2]

    s = smtplib.SMTP(host='smtp.googlemail.com', port=587)
    s.starttls()
    s.login('stockdashboard581@gmail.com', 'stockdashboard')

    msg = MIMEMultipart()

    with app.app_context():
        message = render_template('email.html', sender=sender, recipient=recipient, link=link)

    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = 'Invite to view a Stock Dashboard from {}'.format(sender)

    msg.attach(MIMEText(message, 'html'))
    s.send_message(msg)

    del msg

    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='email_queue', on_message_callback=send_email_message)
channel.start_consuming()
