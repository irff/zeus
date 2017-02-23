FROM alpine:latest
RUN apk update
RUN apk add python py-pip
RUN pip install --upgrade pip

ENV APP_DIR /app

WORKDIR ${APP_DIR}
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY zeus/ zeus
COPY app.py app.py
COPY .env .env

ENV FLASK_APP app.py
EXPOSE 5000
ENTRYPOINT flask run --host=0.0.0.0