#!/bin/bash

# Infinite loop to run the update every 5 minutes
while true; do
    # Send the update request to Duck DNS
    RESPONSE=$(curl -sk "https://www.duckdns.org/update?domains=$DUCKDNS_DOMAIN&token=$DUCKDNS_TOKEN&ip=")
    echo "$(date): $RESPONSE" >> /var/log/duckdns/duckdns.log

    # Wait for 5 minutes
    sleep 300
done