FROM python:3.6-alpine

RUN pip install --upgrade pip

WORKDIR /server

COPY . /server
RUN pip install -r requirements.txt

CMD python server.py
