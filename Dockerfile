FROM python:3.7

WORKDIR /app/ski_conditions

ENV DJANGO_SETTINGS_MODULE ski_conditions.settings
ENV PIPENV_DEPLOY 1
ENV PIPENV_DONT_USE_PYENV 1
ENV PIPENV_SYSTEM 1

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        build-essential \
        gettext \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install pipenv

COPY Makefile /app/ski_conditions
COPY Pipfile /app/ski_conditions
COPY Pipfile.lock /app/ski_conditions
COPY conf/wait-for-it.sh /app/ski_conditions

RUN make requirements

COPY . /app/ski_conditions

RUN mkdir -p /logs \
    && touch /logs/app.log \
    && touch /logs/gunicorn.log

ENV PUBLIC_ROOT /public
ENV LOG_FILE_PATH /logs
ENV ENABLE_LOGGING_TO_FILE true

VOLUME /public/media

EXPOSE 8000

ENTRYPOINT ["/app/ski_conditions/docker-entrypoint.sh"]
