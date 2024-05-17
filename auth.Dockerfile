FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./auth_api/src/requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

COPY ./auth_api/src ./src
COPY ./db ./db
COPY ./settings ./settings

RUN pwd ; ls -al
CMD ["/bin/sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker --chdir src main:app --bind 0.0.0.0:8000"]