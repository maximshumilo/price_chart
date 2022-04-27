FROM python:3.8-slim
WORKDIR /

COPY ./api /api
COPY ./utils /utils
COPY ./config.py /config.py
COPY requirements.txt /requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r /requirements.txt

CMD python3 /api/main.py
