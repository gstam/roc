# FROM python:3.11.0-slim-bulleye AS compile-image
# ARG ENVIRONMENT=development

## update alpine and install build deps 
# RUN set -x \
#     apk update \
#     && apk add --no-cache \
#         gcc \
#         libc-dev \
#         linux-headers \
#         zlib-dev \
#         gtk+3.0-dev \
#         # libjpeg  \
#         musl-dev \
#         mariadb-connector-c-dev \
#         py3-pip \
#         musl-dev \
#         python3-dev \
#         pango-dev \
#         zlib-dev \
#         jpeg-dev \
#         openjpeg-dev \
#         g++ \
#         libffi-dev
#         #mariadb-dev
#         #mariadb-client
#         #postgresql-dev

FROM python:3.11.0-slim-bullseye AS runtime-image
#ARG ENVIRONMENT=development
ARG DEBIAN_FRONTEND=noninteractive

## partially inspired from https://github.com/tiangolo/meinheld-gunicorn-docker

## update Debian and install runtime deps
RUN apt-get update -y &&\
    apt-get install default-libmysqlclient-dev -y  &&\
    apt-get install build-essential -y &&\
    apt-get install nginx -y &&\
    apt-get install vim -y

RUN apt-get -y install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0    

RUN apt-get autoremove -y &&\
    apt-get clean

## virtualenv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

## install requirements
RUN pip install --upgrade pip wheel pip-tools

COPY requirements.txt ./requirements.in

## update requirements file with deployment requirement deps
RUN echo "gunicorn" >> /requirements.in
RUN echo "mysqlclient" >> /requirements.in

RUN pip-compile ./requirements.in > ./requirements.txt \
    && pip-sync \
    && pip install -r ./requirements.txt

## copy Python dependencies from build image
# COPY --from=compile-image /opt/venv /opt/venv

## prepare nginx
COPY docker-files/nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY docker-files/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY docker-files/start.sh /start.sh
RUN chmod +x /start.sh

COPY docker-files/prestart.sh /prestart.sh
RUN chmod +x /prestart.sh

COPY docker-files/gunicorn_conf.py /gunicorn_conf.py

COPY ./roc/ /roc
WORKDIR /roc/


ENV PYTHONPATH=/roc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]

## Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
## And then will start Gunicorn with Meinheld
CMD ["/start.sh"]
