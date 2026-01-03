# Multi-stage build for DigitalOcean App Platform
FROM python:3.11-slim as backend

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Expose port (Railway will set this dynamically)
EXPOSE 8000

# Run the application using shell form to expand $PORT
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}