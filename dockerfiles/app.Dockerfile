ARG PYTHON_VERSION=3.11

ARG APP_DIR="/app"
ARG BUILD_PKGS="curl gcc libc6-dev"
ARG RUNTIME_PKGS="libpq-dev libmagic-dev"


### ベースイメージ ###
FROM python:${PYTHON_VERSION}-slim-bullseye as base

ARG POETRY_HOME="/etc/poetry"

ARG APP_DIR
ARG RUNTIME_PKGS

WORKDIR $APP_DIR

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME=${POETRY_HOME} \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH=${PATH}:${POETRY_HOME}/bin

RUN apt update \
    && apt install --no-install-recommends -y ${RUNTIME_PKGS} \
    && apt autoremove -y \
    && apt autoclean \
    && rm -rf /var/lib/apt/lists/*


### ビルド準備 ###
FROM base as builder

ARG BUILD_PKGS

RUN apt update && \
    apt install --no-install-recommends -y ${BUILD_PKGS} && \
    pip install -U pip && \
    curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --sync


### 開発環境イメージ ###
FROM builder as development

RUN apt install -y --no-install-recommends postgresql-client ssh less vim awscli git make gettext && \
    poetry install --sync

CMD [ "sleep", "infinity" ]


### 実行イメージ ###
FROM base as production

ARG PYTHON_VERSION

COPY src scripts ./

COPY --from=builder /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# CMD [ "./scripts/entrypoint.sh" ]
