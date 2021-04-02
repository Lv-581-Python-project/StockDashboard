FROM python:3.8

COPY . /stock_dashboard_api
WORKDIR /stock_dashboard_api
RUN pip install -r requirements.txt
