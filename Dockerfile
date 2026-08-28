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

# Copy the application.
COPY app ./app

# Ship a starter config; users typically mount their own over this.
COPY config ./config

EXPOSE 5000

CMD ["python", "-m", "app.server"]
