# Use an official lightweight Python runtime
FROM python:3.10-slim

# Set system working directory
WORKDIR /workspace

# Install system dependencies needed for compilation if any
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source files and pre-trained model artifacts
COPY ./app ./app
COPY ./artifacts ./artifacts

# Expose production port
EXPOSE 8000

# Run performance-optimized Uvicorn worker
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
