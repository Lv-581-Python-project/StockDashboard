import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, PackageLoader, select_autoescape

from send_email_queue import connect_queue

connection = connect_queue()
channel = connection.channel()
channel.queue_declare(queue='email_queue', durable=True)


def send_email_message(ch, method, properties, body):
    """
    Sends an email.
    """
    body = json.loads(body)

    sender = body['sender']
    recipient = body['recipient']
    link = os.environ.get('APPLICATION_HOST') + body['path']

    s = smtplib.SMTP(host=os.environ.get('MAIL_HOST'), port=os.environ.get('MAIL_PORT'))
    s.starttls()
    s.login(os.environ.get('MAIL_USERNAME'), os.environ.get('MAIL_PASSWORD'))

    email = MIMEMultipart()

    env = Environment(
        loader=PackageLoader('stock_dashboard_api', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('email.html')
    html = template.render(sender=sender, recipient=recipient, link=link)

    email['From'] = sender
    email['To'] = recipient
    email['Subject'] = 'Invite to view a Stock Dashboard from {}'.format(sender)

    email.attach(MIMEText(html, 'html'))
    s.send_message(email)

    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    channel.basic_consume(queue='email_queue', on_message_callback=send_email_message)
    channel.start_consuming()
