import yagmail
from celery import Celery

MAIL_ID = 'stockdashboard581@gmail.com'
MAIL_PASSWORD = 'stockdashboard'


yag = yagmail.SMTP(MAIL_ID, MAIL_PASSWORD)

app = Celery('send_email', broker='amqp://localhost//',
             include=('send_email',))


@app.task
def send(to, subject, content):
    yag.send(
        to=to,
        subject=subject,
        contents=content,
    )
