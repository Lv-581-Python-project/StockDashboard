FROM python:3.8

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /scheduler
COPY ./workers/scheduler.py .
COPY ./workers/utils ./utils

ENTRYPOINT python /scheduler/scheduler.py