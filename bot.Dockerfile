FROM python:3.12-slim AS build-env

WORKDIR /app
ENV WORKDIR "/app"

COPY ./bot_app/src/requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r ${WORKDIR}/requirements.txt \
    && mkdir -p ${WORKDIR}/logs

#FROM gcr.io/distroless/python3
# I can't use distroless now because an image is old:
# It has a bug in pydantic:
# ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'
# It can be used with python3.11 but my code works only with 3.12.
#WORKDIR /app

ENV WORKDIR "/app"
ENV ENV_FILENAME ".env"
ENV LOG_ENV "prod"
ENV LOG_LEVEL "debug"
ENV PRIVATE_KEY_FILEPATH "${WORKDIR}/keys/private_key.pem"
ENV PUBLIC_KEY_FILEPATH "${WORKDIR}/keys/public_key.pem"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}"

# ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}:/usr/local/lib/python3.12/site-packages"
#COPY --from=build-env /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
#COPY --from=build-env ${WORKDIR}/logs ${WORKDIR}/logs

COPY ./bot_app/src ./bot_app/src
COPY ./auth_app ./auth_app
COPY ./db ./db
COPY ./project_settings ./project_settings
COPY ./helpers ./helpers
COPY ./keys ./keys
COPY ./social_ai_profile_app ./social_ai_profile_app
COPY ./.env ./.env

CMD ["/bin/sh", "-c", "python3 bot_app/src/main.py"]
