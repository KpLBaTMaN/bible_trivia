FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the script to the container
COPY . .

# Install dependencies if necessary (you can skip this if no extra dependencies are needed)
RUN pip install -r requirements.txt

# Run the script by default
# CMD ["python", "populate_db.py"]
CMD ["sh", "-c", "sleep 10 && python populate_db.py"]