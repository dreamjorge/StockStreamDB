# Use the official Python image as a base
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up a working directory
WORKDIR /workspace

# Install Python dependencies
COPY requirements.txt /workspace/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Alembic for migrations
RUN pip install alembic

# Install black (optional for formatting)
RUN pip install black

# Install other project-specific dependencies here if needed

# Expose port 8000 if running a web service or API
EXPOSE 8000

# Default command
CMD [ "bash" ]
