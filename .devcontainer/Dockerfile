# Use the official Python slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /workspaces/StockStreamDB

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install Git, Node.js, npm, and build-essential (for building node-gyp dependencies)
RUN apt-get update && \
    apt-get install -y git curl file unzip build-essential python3 && \
    curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install devcontainer-cli from npm
RUN npm install -g @devcontainers/cli

# Install ajv-cli for JSON Schema validation
RUN npm install -g ajv-cli

# Configure Git to treat the project directory as a safe directory
RUN git config --global --add safe.directory /workspaces/StockStreamDB

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
