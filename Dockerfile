FROM python:3.12 AS dev
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes pipx
ENV PATH="/root/.local/bin:${PATH}"
RUN pipx install poetry
WORKDIR /app
COPY . .
RUN poetry install
CMD ["sleep", "infinity"]

FROM python:3.12 AS builder
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes pipx
ENV PATH="/root/.local/bin:${PATH}"
RUN pipx install poetry
RUN pipx inject poetry poetry-plugin-bundle
WORKDIR /app
COPY . .
# --only==main is a poetry option that specifies to only install non-dev dependencies
RUN poetry bundle venv --python=/usr/bin/python3 --only=main /venv

FROM python:3.12
COPY --from=builder /venv /venv
WORKDIR /app

COPY . .
ENTRYPOINT ["/venv/bin/bookmodeling"]