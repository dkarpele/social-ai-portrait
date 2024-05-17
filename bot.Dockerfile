FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/${WORKDIR}"

COPY ./bot/src/requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

COPY ./bot/src ./src
COPY ./db ./db
COPY ./settings ./settings

RUN pwd ; ls -al
CMD ["/bin/sh", "-c", "python3 src/main.py"]
