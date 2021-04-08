import json

from flask import render_template, redirect, url_for, request, Blueprint

from stock_dashboard_api.forms import EmailForm
from stock_dashboard_api.utils.send_email_queue import publish_email

mod = Blueprint('dashboard', __name__, url_prefix='/mail')


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

        body = json.dumps({"sender": sender,
                           "recipient": recipient,
                           "path": path,
                           "template_name": "dashboard_invite_email"})
        publish_email(body)

        return redirect(url_for('dashboard.home'))
    return render_template('send_email.html', form=form)
