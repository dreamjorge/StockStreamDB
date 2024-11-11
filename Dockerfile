# Use a specific, minimal version of the Python image for reduced attack surface
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install necessary packages securely
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        file \
        git \
        unzip && \
    # Install Node.js securely using HTTPS with verification
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    # Clean up APT caches to reduce image size and prevent potential leaks
    rm -rf /var/lib/apt/lists/*

# Install npm packages with --ignore-scripts to prevent execution of shell scripts
RUN npm install -g @devcontainers/cli --ignore-scripts && \
    npm install -g ajv-cli --ignore-scripts

# Configure Git to treat the project directory as a safe directory
RUN git config --global --add safe.directory /workspaces/StockStreamDB

# Set the working directory to the project directory
WORKDIR /workspaces/StockStreamDB

# Copy only necessary project files, excluding sensitive data
# The .dockerignore file ensures that sensitive files are not copied
COPY --chown=root:root . .

# Upgrade pip to the latest version to ensure compatibility and security
RUN pip install --upgrade pip

# Install your Python package using pip without caching to reduce image size
RUN pip install --no-cache-dir .

# Create a local .czrc configuration in the project directory with appropriate ownership
RUN echo '{ "path": "/usr/lib/node_modules/cz-conventional-changelog" }' > .czrc

# Ensure no write permissions are assigned to the copied files to enhance security
RUN chmod -R a-w /workspaces/StockStreamDB

# Create a non-root user to run the application for enhanced security
RUN useradd -ms /bin/bash nonroot

# Switch to the non-root user to run subsequent commands
USER nonroot

# Explicitly set PYTHONPATH without referencing the previous value to avoid unintended inheritance
ENV PYTHONPATH="/workspaces/StockStreamDB/src"

# Set the default command to run the CLI tool
CMD ["stockstreamdb", "--help"]
