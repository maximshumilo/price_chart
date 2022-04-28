FROM python:3.9-slim

COPY worker /usr/src/app/worker
COPY utils /usr/src/app/utils
COPY config.py /usr/src/app/config.py
COPY requirements.txt /usr/src/app/requirements.txt

ENV PYTHONPATH=/usr/src/app
WORKDIR /usr/src/app

RUN chmod +x worker/docker-entrypoint.sh && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["/usr/src/app/worker/docker-entrypoint.sh"]