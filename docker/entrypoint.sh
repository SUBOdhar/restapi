#!/bin/bash

# Function to clone auth.py from GitHub
clone_auth() {
    git clone https://github.com/your_username/your_repo.git /app
}

# Function to check if auth.py is older than 7 days
is_auth_old() {
    find "/app/auth.py" -mtime +7 &> /dev/null
}

# Check if auth.py exists and is older than 7 days
if [ ! -f "/app/auth.py" ] || is_auth_old; then
    echo "Fetching auth.py from GitHub"
    rm -f /app/auth.py
    clone_auth
else
    echo "auth.py exists and is less than 7 days old, skipping fetch"
fi

# Start cron service in the background
service cron start

# Add a cron job to clone auth.py every 7 days
echo "0 0 * * * root /app/entrypoint.sh" > /etc/cron.d/clone_auth

# Apply cron job settings
crontab /etc/cron.d/clone_auth

# Run the Python application
exec python /app/auth.py
