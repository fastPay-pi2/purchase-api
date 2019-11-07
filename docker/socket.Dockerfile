FROM python:3.7-slim

WORKDIR /usr/src/app

ADD ./docker/socket.requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

ADD ./purchase_socket /usr/src/app

CMD python app.py