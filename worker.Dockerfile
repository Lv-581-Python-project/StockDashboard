FROM python:3.8

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /worker
COPY ./workers/worker.py .
COPY ./workers/utils ./utils

ENTRYPOINT python /worker/worker.py