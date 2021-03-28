from StockDashboardAPI import app
from flask import render_template, redirect, url_for, request
from .rabbit_channel import get_email_queue
from .forms import EmailForm
import pika


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/send_email', methods=['GET', 'POST'])
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
