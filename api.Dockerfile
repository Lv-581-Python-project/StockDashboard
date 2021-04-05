FROM python:3.8

WORKDIR /stock_dashboard_api
COPY . /stock_dashboard_api
COPY requirements_api.txt requirements.txt

RUN pip install -r requirements.txt
