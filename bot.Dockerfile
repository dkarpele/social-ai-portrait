FROM python:3.12

WORKDIR /app

ENV WORKDIR "/app"
ENV ENV_FILENAME ".env"
ENV LOG_ENV "prod"
ENV LOG_LEVEL "info"
ENV PRIVATE_KEY_FILEPATH "${WORKDIR}/keys/private_key.pem"
ENV PUBLIC_KEY_FILEPATH "${WORKDIR}/keys/public_key.pem"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}"

COPY ./bot_app/src/requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt \
    && mkdir -p ${WORKDIR}/logs

COPY ./bot_app/src ./bot_app
COPY ./auth_app ./auth_app
COPY ./db ./db
COPY ./settings ./settings
COPY ./helpers ./helpers
COPY ./keys ./keys
COPY ./social_ai_portrait_app ./social_ai_portrait_app


CMD ["/bin/sh", "-c", "python3 bot_app/main.py"]
