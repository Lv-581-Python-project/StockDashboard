from flask import render_template, redirect, url_for, request, Blueprint
from stock_dashboard_api.rabbit.send_email_queue import get_email_queue
from stock_dashboard_api.forms import EmailForm
import pika


mod = Blueprint('dashboard', __name__, url_prefix='/mail')


@mod.route('/')
@mod.route('/home')
def home():
    return render_template('home.html')


@mod.route('/send_email', methods=['GET', 'POST'])
def send_email():
    form = EmailForm()
    if form.validate_on_submit():

        sender = form.sender.data
        recipient = form.recipient.data
        path = request.endpoint

        body = sender + ' ' + recipient + ' ' + path

        queue = get_email_queue()
        queue.basic_publish(
            exchange='amq.direct',
            routing_key='email_queue',
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        return redirect(url_for('home'))
    return render_template('send_email.html', form=form)
