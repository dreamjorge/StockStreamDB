FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project files
COPY . .

# Default command to run the CLI
CMD ["python", "src/interfaces/cli/cli.py", "--help"]
