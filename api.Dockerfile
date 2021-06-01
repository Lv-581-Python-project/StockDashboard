FROM python:3.8

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /
COPY ./stock_dashboard_api/ /stock_dashboard_api/

ENTRYPOINT flask run --host=0.0.0.0 --port=5000
