# ------------------------------------------------------------------------------
# Stage 1: Fetch frontend assets
# ------------------------------------------------------------------------------

FROM node:lts-slim AS frontend-assets

WORKDIR /build

RUN corepack enable

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY scripts/provision-bootstrap.sh scripts/provision-bootstrap.sh
RUN pnpm provision

# ------------------------------------------------------------------------------
# Stage 2: Fetch Python packages
# ------------------------------------------------------------------------------

FROM python:3.14-slim AS python-venv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_NO_INSTALL_PROJECT=1 \
    UV_LINK_MODE=copy

# Install uv
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

# Create virtual environment
RUN uv venv

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# ------------------------------------------------------------------------------
# Stage 3: Runner
# ------------------------------------------------------------------------------

FROM python:3.14-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1\
    CONFIG_PATH=/app/config/example.yaml

# Copy the provisioned Bootstrap assets from the Node stage.
COPY --from=frontend-assets /build/app/static/bootstrap ./app/static/bootstrap
COPY --from=frontend-assets /build/app/static/bootstrap-icons ./app/static/bootstrap-icons

# Copy virtual environment and add to PATH
COPY --from=python-venv /app/.venv ./.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application.
COPY app ./app

# Ship an example config
COPY config/example.yaml ./config/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "30", "app.server:app"]
