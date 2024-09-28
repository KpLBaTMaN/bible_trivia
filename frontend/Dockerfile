# FROM python:3.9-slim

# WORKDIR /app

# COPY ./ /app

# RUN pip install --no-cache-dir -r ./requirements.txt

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


# frontend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend code
COPY ./ /app/

# Expose port
EXPOSE 80

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
