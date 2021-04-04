import os
import tempfile
import requests

import pytest

from stock_dashboard_api import stock_dashboard_api
from pytest_rabbitmq import factories

rabbitmq_my_proc = factories.rabbitmq_proc(
    port=8888, logsdir='/tmp'
)
rabbitmq_my = factories.rabbitmq('rabbitmq_my_proc')


@pytest.fixture
def client():
    db_fd, stock_dashboard_api.app.config['DATABASE'] = tempfile.mkstemp()
    stock_dashboard_api.app.config['TESTING'] = True

    with stock_dashboard_api.app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(stock_dashboard_api.app.config['DATABASE'])


def test_homepage(client):
    response = client.get('/mail/home')
    assert b'This is the home page' in response.data


def test_send_email_get(client):
    response = client.get('/mail/send_email')
    assert b'I am the dashboard page.' in response.data


def test_send_email_post(client):
    data = {
        "sender": "Test",
        "recipient": "test_stock_dashboard581@gmail.com",
    }
    response = requests.post("http://127.0.0.1:5000/mail/send_email", data=data)
    print(response.content)

    assert b'This is the home page' in response.content
    assert response.status_code == 200
