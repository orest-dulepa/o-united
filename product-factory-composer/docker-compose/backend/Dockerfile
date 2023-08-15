FROM python:3.9.1-buster

COPY backend/requirements /requirements
COPY backend/requirements.txt /

RUN pip install -r /requirements.txt

RUN rm -rf /requirements

COPY docker-compose/backend/entrypoint.sh /

RUN chmod +x /entrypoint.sh

WORKDIR /app

ENTRYPOINT [ "/entrypoint.sh" ]
