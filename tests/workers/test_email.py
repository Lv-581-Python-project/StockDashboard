import json
import os

import pika
import pytest
from pytest_rabbitmq import factories

from stock_dashboard_api import app
from workers.email_sender.send_email_worker import create_email


@pytest.fixture
def client():
    app.config['TESTING'] = True
    rabbitmq_my_proc = factories.rabbitmq_proc(port=8888)
    rabbitmq = factories.rabbitmq('rabbitmq_my_proc')

    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get('/mail/home')
    assert b'This is the home page' in response.data


def test_send_email_get(client):
    response = client.get('/mail/send_email')
    assert b'This is the dashboard page.' in response.data


def test_send_email_post(client):
    app.config['WTF_CSRF_ENABLED'] = False
    data = {
        "sender": "Test",
        "recipient": "test_stock_dashboard581@gmail.com",
    }
    response = client.post('/mail/send_email', data=data, follow_redirects=True)

    assert b'This is the home page' in response.data
    assert response.status_code == 200


def test_send_email_invalid_no_sender(client):
    app.config['WTF_CSRF_ENABLED'] = False
    data = {
        "sender": "",
        "recipient": "test_stock_dashboard581@gmail.com",
    }
    response = client.post('/mail/send_email', data=data, follow_redirects=True)

    assert b'This field is required' in response.data
    assert response.status_code == 200


def test_send_email_invalid_no_recipient(client):
    app.config['WTF_CSRF_ENABLED'] = False
    data = {
        "sender": "Test",
        "recipient": "",
    }
    response = client.post('/mail/send_email', data=data, follow_redirects=True)

    assert b'This field is required' in response.data
    assert response.status_code == 200


def test_send_email_invalid_no_data(client):
    app.config['WTF_CSRF_ENABLED'] = False
    data = {
        "sender": "",
        "recipient": "",
    }
    response = client.post('/mail/send_email', data=data, follow_redirects=True)

    assert b'This field is required' in response.data
    assert response.status_code == 200


def test_create_email_function():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ.get('RABBITMQ_CONNECTION_HOST'))
    )
    channel = connection.channel()

    class Method:
        delivery_tag = 0

    method = Method

    body = json.dumps({"sender": 'Test',
                       "recipient": 'test_stock_dashboard581@gmail.com',
                       "path": 'http://127.0.0.1:5000/mail/send_email',
                       "template_name": "dashboard_invite_email"})

    sent = create_email(ch=channel, method=method, properties=pika.BasicProperties(delivery_mode=2), body=body)
    assert sent is True
