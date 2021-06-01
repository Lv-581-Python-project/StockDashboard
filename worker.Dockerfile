FROM python:3.8

ADD requirements.txt /
RUN pip install -r requirements.txt

WORKDIR .
COPY ./workers/worker.py ./workers/worker.py
COPY ./workers/workers_utils ./workers/workers/workers_utils
ENV LOGGING_CONF=./workers/workers/workers_utils/logging.conf
ENTRYPOINT python ./workers/worker.py
