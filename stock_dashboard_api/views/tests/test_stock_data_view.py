import pytest
import requests
import json

def test_get_pass():
    response = requests.get('http://127.0.0.1:5000/stocks_data/1')
    print(response.json()['id'])
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['create_at'] == '2021-01-01'
    assert response.json()['price'] == 300
    assert response.json()['stock_id'] == 2


def test_get_fail():
    response = requests.get('http://127.0.0.1:5000/stocks_data/2')
    assert response.status_code == 400
    assert response.text == "Can not find stock data, wrong id"


def test_post_pass():
    data = json.dumps({"stock_id": 3,
            "price": 300,
            "create_at": "2020-01-01"})
    response = requests.post('http://127.0.0.1:5000/stocks_data/', json=data)
    assert response.status_code == 201
    assert response.json()['id'] == 1
    assert response.json()['create_at'] == '2020-01-01'
    assert response.json()['price'] == 300
    assert response.json()['stock_id'] == 3

def test_post_fail():
    incorrect_json = '{ name":"John "age":30 "car:"None" }'
    response = requests.post('http://127.0.0.1:5000/stocks_data/', json=incorrect_json)
    assert response.status_code == 400
    assert response.text == "Invalid JSON"

    response = requests.post('http://127.0.0.1:5000/stocks_data/')
    assert response.status_code == 400
    assert response.text == "No data provided"

    data = json.dumps({"stock_id": 3,
                       "price": 300
                       })
    response = requests.post('http://127.0.0.1:5000/stocks_data/',json=data)
    assert response.status_code == 400
    assert response.text == "Stock data is not created"

