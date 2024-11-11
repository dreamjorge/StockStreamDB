# Builder Stage
FROM python:3.9-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        unzip && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

RUN npm install -g @devcontainers/cli --ignore-scripts && \
    npm install -g ajv-cli --ignore-scripts

WORKDIR /workspaces/StockStreamDB

COPY --chown=root:root . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir . && \
    echo '{ "path": "/usr/lib/node_modules/cz-conventional-changelog" }' > .czrc && \
    chmod -R a-w /workspaces/StockStreamDB

# Final Stage
FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

RUN npm install -g @devcontainers/cli --ignore-scripts && \
    npm install -g ajv-cli --ignore-scripts

RUN useradd -ms /bin/bash nonroot

WORKDIR /workspaces/StockStreamDB

COPY --from=builder /workspaces/StockStreamDB /workspaces/StockStreamDB

USER nonroot

ENV PYTHONPATH="/workspaces/StockStreamDB/src"

CMD ["stockstreamdb", "--help"]
