"""
Send email worker
"""

import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, PackageLoader, select_autoescape

from send_email_queue import connect_queue


def create_email(ch, method, properties, body):
    """
    Generates an email to send.
    """
    body = json.loads(body)

    sender = body['sender']
    recipient = body['recipient']
    link = os.environ.get('APPLICATION_HOST') + body['path']
    template_name = body['template_name']

    email = MIMEMultipart()

    env = Environment(
        loader=PackageLoader('workers', 'email_sender/templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(template_name + '.html')
    html = template.render(sender=sender, recipient=recipient, link=link)

    email['From'] = sender
    email['To'] = recipient
    email['Subject'] = 'Invite to view a Stock Dashboard from {}'.format(sender)
    email.attach(MIMEText(html, 'html'))

    send_email(ch, email, properties, method)


def send_email(ch, email, properties, method):  # pylint: disable=C0103,  W0613
    """
    Sends an email.
    """
    smtp_conn = smtplib.SMTP(host=os.environ.get('MAIL_HOST'), port=os.environ.get('MAIL_PORT'))
    smtp_conn.starttls()
    smtp_conn.login(os.environ.get('MAIL_USERNAME'), os.environ.get('MAIL_PASSWORD'))
    smtp_conn.send_message(email)

    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = connect_queue()
    channel = connection.channel()
    channel.queue_declare(queue='email_queue', durable=True)
    channel.basic_consume(queue='email_queue', on_message_callback=create_email)
    channel.start_consuming()
