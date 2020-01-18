# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.6-alpine3.9

RUN apk add --update npm
RUN npm -v
RUN node -v

# dev dependencies
RUN apk add --no-cache \
        musl-dev \
        python3-dev \
        libffi-dev \
        openssl-dev \
        mariadb-dev \
        postgresql-dev \
        libxml2-dev \
        libxslt-dev \
        tiff-dev \
        zlib-dev

# other dependencies
RUN apk add --no-cache \
        gcc \
        git \
        gettext \
        linux-headers \
        libmagic \
        libjpeg \
        wkhtmltopdf \
        make

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/srv/app"


# Django dirs
RUN mkdir -p /srv/app /srv/www/static /srv/www/media
VOLUME [ "/srv/www" ]

WORKDIR /srv/app
EXPOSE 8082

# Copy the current directory contents into the container
COPY ./backend/requirements.txt /requirements.txt
COPY ./ /srv/app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip setuptools && pip install -r /requirements.txt
