FROM python:3.8

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /worker
COPY ./workers/worker.py .
COPY ./workers/workers_utils ./workers_utils

ENTRYPOINT python /worker/worker.py