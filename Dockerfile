# Use a specific version of the python image
FROM python:3.9-slim

# Create a non-root user
RUN useradd -ms /bin/bash nonroot

# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl file unzip build-essential python3 && \
    curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install devcontainer-cli from npm
RUN npm install -g @devcontainers/cli --ignore-scripts

# Install ajv-cli for JSON Schema validation
RUN npm install -g ajv-cli --ignore-scripts

# Configure Git to treat the project directory as a safe directory
RUN git config --global --add safe.directory /workspaces/StockStreamDB

# Switch to the non-root user
USER nonroot

# Copy the rest of the project files into the container
COPY . .

# Explicitly set PYTHONPATH without referencing the previous value
ENV PYTHONPATH="/workspaces/StockStreamDB/src"

# Install your package using setup.py (or pyproject.toml)
RUN pip install .

# Create a local .czrc configuration in the project directory
RUN echo '{ "path": "/usr/lib/node_modules/cz-conventional-changelog" }' > /workspaces/StockStreamDB/.czrc

# Set the default command to run the CLI tool
CMD ["stockstreamdb", "--help"]
