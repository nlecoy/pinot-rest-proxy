FROM python:3.8.2-slim as python-base

LABEL MAINTAINER="Nicolas Lecoy <nicolas.lecoy@gmail.com>"

ARG COMMIT

ENV BUILD_REVISION $COMMIT
ENV PIP_DEFAULT_TIMEOUT 100
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_NO_CACHE_DIR off
ENV POETRY_VERSION 1.1.4
ENV POETRY_HOME /opt/poetry
ENV POETRY_NO_INTERACTION 1
ENV POETRY_VIRTUALENVS_IN_PROJECT true
ENV PYSETUP_PATH /opt/pysetup
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VENV_PATH /opt/pysetup/.venv

ENV PATH $POETRY_HOME/bin:$VENV_PATH/bin:$PATH

FROM python-base as builder-base

RUN apt-get update && apt-get install --no-install-recommends -y \
  curl \
  build-essential

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR $PYSETUP_PATH

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry install --no-dev --no-root

# Copy source directory, README.md file and run poetry install again to make sure
# that the module 'pinot_rest_proxy' gets installed.
COPY README.md README.md
COPY pinot_rest_proxy pinot_rest_proxy

RUN poetry install --no-dev

FROM python-base as production

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./pinot_rest_proxy /usr/src/pinot_rest_proxy/

WORKDIR /usr/src

CMD ["sanic", "pinot_rest_proxy.asgi.app", "--host=0.0.0.0"]
