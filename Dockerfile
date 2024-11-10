# Use a specific version of the python image
FROM python:3.9-slim

# Create a non-root user
RUN useradd -ms /bin/bash nonroot

# Install necessary packages securely
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        file \
        git \
        python3 \
        unzip && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install devcontainer-cli from npm with ignore-scripts for security
RUN npm install -g @devcontainers/cli --ignore-scripts

# Install ajv-cli for JSON Schema validation with ignore-scripts for security
RUN npm install -g ajv-cli --ignore-scripts

# Configure Git to treat the project directory as a safe directory
RUN git config --global --add safe.directory /workspaces/StockStreamDB

# Switch to the non-root user
USER nonroot

# Copy only necessary project files, excluding sensitive data
# Ensure no write permissions are assigned to the copied files
COPY --chown=nonroot:nonroot . .
RUN chmod -R a-w /workspaces/StockStreamDB

# Explicitly set PYTHONPATH without referencing the previous value
ENV PYTHONPATH="/workspaces/StockStreamDB/src"

# Install your package using setup.py (or pyproject.toml)
RUN pip install .

# Create a local .czrc configuration in the project directory
RUN echo '{ "path": "/usr/lib/node_modules/cz-conventional-changelog" }' > /workspaces/StockStreamDB/.czrc

# Set the default command to run the CLI tool
CMD ["stockstreamdb", "--help"]
