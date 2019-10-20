FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY ./database_population  .

RUN pip install -r requirements.txt

CMD ["python", "popula_purchases.py"]