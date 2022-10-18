FROM python:3.10-slim-buster AS environment

ENV LANG=C.UTF-8 \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.1.13

WORKDIR /scanner

RUN apt-get update \
    && apt-get install -y libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry==$POETRY_VERSION"

RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./

RUN poetry export --format requirements.txt --output fulldependencies.txt --without-hashes && \
    /venv/bin/pip install --requirement fulldependencies.txt && \
    rm fulldependencies.txt

# --------------------------------------------------------

FROM python:3.10-slim-buster AS final

ENV LANG=C.UTF-8

RUN apt-get update \
    && apt-get install -y \
        libgl1-mesa-dev \
        libtesseract-dev \
        tesseract-ocr \
        tesseract-ocr-spa \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /scanner

COPY --from=environment /venv /venv

ENV PATH="/venv/bin:$PATH"

COPY docker/entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["/usr/bin/entrypoint.sh"]

COPY . .

# Run as non-root user
RUN useradd -m non-root-user
USER non-root-user
