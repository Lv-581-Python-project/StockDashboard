from flask import Flask
from flask_mail import Mail
from .config import DevelopmentConfig

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
app.config.update(dict(
    MAIL_SERVER='smtp.googlemail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=1,
    MAIL_USERNAME='stockdashboard581@gmail.com',
    MAIL_PASSWORD='stockdashboard',
))

mail = Mail(app)

from StockDashboardAPI import routes
