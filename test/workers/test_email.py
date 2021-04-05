import pytest
from pytest_rabbitmq import factories

from stock_dashboard_api import stock_dashboard_api

rabbitmq_my_proc = factories.rabbitmq_proc(
    port=8888, logsdir='/tmp'
)
rabbitmq_my = factories.rabbitmq('rabbitmq_my_proc')


@pytest.fixture
def client():
    stock_dashboard_api.app.config['TESTING'] = True

    with stock_dashboard_api.app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get('/mail/home')
    assert b'This is the home page' in response.data


def test_send_email_get(client):
    response = client.get('/mail/send_email')
    assert b'This is the dashboard page.' in response.data


def test_send_email_post(client):
    data = {
        "sender": "Test",
        "recipient": "test_stock_dashboard581@gmail.com",
    }
    response = client.post("http://127.0.0.1:5000/mail/send_email", data=data, follow_redirects=True)

    assert b'This is the home page' in response.data
    assert response.status_code == 200


def test_send_email_invalid_no_sender(client):
    data = {
        "sender": "",
        "recipient": "test_stock_dashboard581@gmail.com",
    }
    response = client.post("http://127.0.0.1:5000/mail/send_email", data=data, follow_redirects=True)

    assert b'This field is required' in response.data
    assert response.status_code == 200


def test_send_email_invalid_no_recipient(client):
    data = {
        "sender": "Test",
        "recipient": "",
    }
    response = client.post("http://127.0.0.1:5000/mail/send_email", data=data, follow_redirects=True)

    assert b'This field is required' in response.data
    assert response.status_code == 200


def test_send_email_invalid_no_data(client):
    data = {
        "sender": "",
        "recipient": "",
    }
    response = client.post("http://127.0.0.1:5000/mail/send_email", data=data, follow_redirects=True)

    assert b'This field is required' in response.data
    assert response.status_code == 200
