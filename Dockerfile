# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Add entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Grant execution permissions to the entrypoint script
RUN chmod +x /app/entrypoint.sh

# Run entrypoint.sh when the container launches
ENTRYPOINT ["/app/entrypoint.sh"]
