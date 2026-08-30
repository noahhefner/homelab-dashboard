# Stage 1: provision Bootstrap assets (Node + pnpm). Keeps the runtime image
# free of Node by producing only the compiled assets consumed by Stage 2.
FROM node:22-slim AS bootstrap-assets

WORKDIR /build

# Enable pnpm via corepack (pinned / reproducible).
RUN corepack enable

# Install dependencies from the committed lockfile (deterministic).
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Copy the provisioning script and materialize the served assets.
COPY scripts/provision-bootstrap.sh scripts/provision-bootstrap.sh
RUN pnpm provision

FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/usr/local \
    CONFIG_PATH=/app/config/example.yaml

WORKDIR /app

# Install uv (single binary, no pip).
COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /uvx /usr/local/bin/

# Install dependencies without reinstalling the (non-package) project.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy the provisioned Bootstrap assets from the Node stage.
COPY --from=bootstrap-assets /build/app/static/bootstrap ./app/static/bootstrap
COPY --from=bootstrap-assets /build/app/static/bootstrap-icons ./app/static/bootstrap-icons

# Copy the application.
COPY app ./app

# Ship a starter config; users typically mount their own over this.
COPY config ./config

EXPOSE 5000

CMD ["python", "-m", "app.server"]
