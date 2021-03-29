import pika
from flask_mail import Message

from StockDashboardAPI import app, mail

DOMAIN = 'example.com'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue', durable=True)


def send_email_message(ch, method, properties, body):
    body = body.decode('utf-8')
    body = body.split(' ')
    sender = body[0]
    recipient = body[1]
    link = 'http://127.0.0.1:5000/' + body[2]
    print('Sending email to {}'.format(recipient))  # change to address
    # template = render_template('email.html',
    #                            sender='stockdashboard581@gmail.com',
    #                            recipient=recipient,
    #                            link=link)
    template = "<html><head><style>* {margin: 0;padding: 0;}" \
               ".flex-center {display: flex;align-items: center;justify-content: center;}" \
               ".header {background-color: lightblue;color: white;" \
               ".link {text-decoration: none;color: #2C66E1;}</style>" \
               "</head>" \
               "<body><div class='header flex-center'><h1>Hello %s!</h1></div>" \
               "<p class='flex-center' style='color: blue;'>" \
               "You've been invited to view a Stock Dashboard at the following link by %s:</p>" \
               "<p class='flex-center link'>%s</p></body></html>" % (recipient, sender, link)
    msg = Message(html=template,
                  subject='Hello {}'.format(recipient),
                  sender='stockdashboard581@gmail.com',
                  recipients=[recipient]
                  )

    with app.app_context():
        mail.send(msg)
    channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='email_queue', on_message_callback=send_email_message)
channel.start_consuming()
