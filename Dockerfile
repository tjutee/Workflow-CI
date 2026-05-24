# Dockerfile untuk MLflow Project
# Image ini dapat di-build dengan: docker build -t customer-segmentation:latest .

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY MLProject /app/MLProject
COPY conda.yaml /app/
COPY modelling.py /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r MLProject/requirements.txt || \
    pip install mlflow scikit-learn pandas matplotlib numpy

# Create data directory
RUN mkdir -p /app/data /app/mlruns /app/artifacts

# Set environment variables
ENV MLFLOW_TRACKING_URI=/app/mlruns
ENV PYTHONUNBUFFERED=1

# Entry point
ENTRYPOINT ["python", "modelling.py"]
CMD ["--help"]
