FROM nginx:alpine AS build-env
COPY ./www /var/www/
