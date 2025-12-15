FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed for some libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY main.py .

# Create directories for data and output
RUN mkdir -p data output

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "main.py"]
