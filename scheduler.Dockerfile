FROM python:3.8

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /
COPY ./workers/scheduler_worker.py /scheduler.py

ENTRYPOINT python /scheduler.py