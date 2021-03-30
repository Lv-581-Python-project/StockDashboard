import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pika
from dotenv import load_dotenv
from flask import render_template

from StockDashboardAPI import app

project_folder = os.getcwd()
load_dotenv(os.path.join(project_folder, '../.env'))

connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_CONNECTION_HOST')))
channel = connection.channel()
channel.queue_declare(queue='email_queue', durable=True)


def send_email_message(ch, method, properties, body):
    body = body.decode('utf-8')
    body = body.split(' ')

    sender = body[0]
    recipient = body[1]
    link = 'http://127.0.0.1:5000/' + body[2]

    s = smtplib.SMTP(host=os.getenv('MAIL_HOST'), port=os.getenv('MAIL_PORT'))
    s.starttls()
    s.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))

    msg = MIMEMultipart()

    with app.app_context():
        template = render_template('email.html', sender=sender, recipient=recipient, link=link)

    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = 'Invite to view a Stock Dashboard from {}'.format(sender)

    msg.attach(MIMEText(template, 'html'))
    s.send_message(msg)

    del msg

    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='email_queue', on_message_callback=send_email_message)
channel.start_consuming()
