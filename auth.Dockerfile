FROM python:3.12

WORKDIR /app

ENV WORKDIR "/app"
ENV ENV_FILENAME ".env"
ENV PRIVATE_KEY_FILEPATH "${WORKDIR}/keys/private_key.pem"
ENV PUBLIC_KEY_FILEPATH "${WORKDIR}/keys/public_key.pem"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}"

COPY ./auth_api/src/requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

COPY ./auth_api/src ./auth_api
COPY ./auth_app ./auth_app
COPY ./db ./db
COPY ./settings ./settings
COPY ./helpers ./helpers
COPY ./keys ./keys

RUN pwd ; ls -al
CMD ["/bin/sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker --chdir auth_api main:app --bind 0.0.0.0:8000"]