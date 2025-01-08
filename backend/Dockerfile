# Use the official Python 3.11.11 (slim) image as the base
FROM python:3.11.11-slim AS base

# Prevent Python from writing .pyc files to disk and enable unbuffered stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code into the image
COPY . /app

# Expose port 8000 for FastAPI
EXPOSE 8000

# Default command: run the main FastAPI module
CMD ["python", "-m", "app.main"]
