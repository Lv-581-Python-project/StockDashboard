from flask import Flask
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

CKEDITOR_ENABLE_CSRF = True

app.config['SECRET_KEY'] = 'SDQ(*&SD(*Q(899*DS98(*&8978sd7987s98d7q9*Q'

# from app import routes
