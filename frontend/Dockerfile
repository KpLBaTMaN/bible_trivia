# frontend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend code
COPY . .

# Expose port
EXPOSE 80

# Start the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
