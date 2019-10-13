FROM python:3.7-slim

WORKDIR /usr/src/app

ADD ./docker/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

ADD ./purchase_api /usr/src/app

CMD python manage.py run -h 0.0.0.0