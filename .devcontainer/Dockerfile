FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


RUN apt-get update && \
    apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g commitizen && \
    npm install --save-dev cz-conventional-changelog

    
# Copy the project files
COPY . .

# Default command to run the CLI
CMD ["python", "src/interfaces/cli/cli.py", "--help"]
