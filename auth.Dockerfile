FROM python:3.12

WORKDIR /app

ENV WORKDIR "/app"
ENV ENV_FILENAME ".env"
ENV LOG_ENV "prod"
ENV LOG_LEVEL "debug"
ENV PRIVATE_KEY_FILEPATH "${WORKDIR}/keys/private_key.pem"
ENV PUBLIC_KEY_FILEPATH "${WORKDIR}/keys/public_key.pem"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}"

COPY ./auth_api/src/requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt \
    && mkdir -p ${WORKDIR}/logs

COPY ./auth_api/src ./auth_api/src
COPY ./auth_app ./auth_app
COPY ./db ./db
COPY ./settings ./settings
COPY ./helpers ./helpers
COPY ./keys ./keys

RUN pwd ; ls -al

CMD ["/bin/sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker --logger-class=auth_api.src.core.config.GunicornLogger --log-level DEBUG --bind 0.0.0.0:8000 auth_api.src.main:app"]
