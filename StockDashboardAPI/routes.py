import send_email
from app import app


@app.route('/send_email', methods=['GET', 'POST'])
def send_emails():
    send_email.send.delay(
        'slavko.dem@gmail.com',
        'Testing sending email',
        'Test successful!'
    )
    return 'sending emails'
