#!/bin/sh
# run.sh





# # Wait for 5 seconds before starting
# sleep 5

# # Run the create_admin.py script
# echo "Starting create_admin.py..."
# python create_admin.py
# echo "create_admin.py completed."

# # Wait for 10 seconds before the next script
# sleep 10

# # Run the populate_db.py script
# echo "Starting populate_db.py..."
# python populate_db.py
# echo "populate_db.py completed."





# Wait for 5 seconds before the next script
sleep 5

# Run the bulk_upload_questions_json.py script
echo "Starting bulk_upload_questions_json.py..."
python bulk_upload_questions_json.py
echo "bulk_upload_questions_json.py completed."

# Optional: Keep the container running if needed
# tail -f /dev/null
