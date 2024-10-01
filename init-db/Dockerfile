FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the script to the container
COPY . .

# Install dependencies if necessary (you can skip this if no extra dependencies are needed)
RUN pip install -r requirements.txt

# Run the script by default
# CMD ["python", "populate_db.py"]
# CMD ["sh", "-c", "sleep 10 && python populate_db.py && python create_admin.py"]
# CMD ["sh", "-c", "sleep 10 && python create_admin.py"]

# Run the scripts sequentially
# CMD sh -c "sleep 10 && python create_admin.py && sleep 15 && python populate_db.py"
# CMD sh -c "sleep 5 && python create_admin.py && echo 'create_admin.py completed' && sleep 10 && python populate_db.py"
# CMD sh -c "sleep 5 && python bulk_upload_questions_json.py"

# Set the default command to execute the run.sh script
CMD ["sh", "run.sh"]