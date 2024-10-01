# Use a lightweight base image
FROM alpine:latest

# Install curl and bash
RUN apk add --no-cache curl bash

# Copy the update script into the container
COPY duck.sh /duck.sh

# Make the script executable
RUN chmod +x /duck.sh

# Set the entrypoint to run the script
ENTRYPOINT ["/duck.sh"]
