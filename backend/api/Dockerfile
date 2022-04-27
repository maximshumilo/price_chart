FROM python:3.9-slim

COPY api /usr/src/app/api
COPY utils /usr/src/app/utils
COPY config.py /usr/src/app/config.py
COPY requirements.txt /usr/src/app/requirements.txt

ENV PYTHONPATH=/usr/src/app
WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install -r /usr/src/app/requirements.txt

EXPOSE 5000
CMD python api/main.py
