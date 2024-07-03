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

COPY ./requirements.txt requirements.txt
COPY ./entrypoint.sh entrypoint.sh
COPY ./keys ./keys

RUN pip install --upgrade pip \
    && pip install -r ${WORKDIR}/requirements.txt

CMD ["/bin/sh", "-c", "pytest -s -v --disable-warnings ${WORKDIR}/test_apps/end_to_end/src"]