from flask import render_template, redirect, url_for, request, Blueprint
from workers.email_sender.send_email_queue import get_email_queue
from stock_dashboard_api.forms import EmailForm
import pika
import json

mod = Blueprint('dashboard', __name__, url_prefix='/mail')

RABBITMQ_DELIVERY_MODE = 2


@mod.route('/')
@mod.route('/home')
def home():
    """
    Temporary main page.
    """
    return render_template('home.html')


@mod.route('/send_email', methods=['GET', 'POST'])
def send_email():
    """
    Handles a form that is used to send an email.
    """
    form = EmailForm()
    if form.validate_on_submit():

        sender = form.sender.data
        recipient = form.recipient.data
        path = request.endpoint

        body = json.dumps({"sender": sender, "recipient": recipient, "path": path})

        queue = get_email_queue()
        queue.basic_publish(
            exchange='email',
            routing_key='email_queue',
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=RABBITMQ_DELIVERY_MODE,
            )
        )
        return redirect(url_for('dashboard.home'))
    return render_template('send_email.html', form=form)
