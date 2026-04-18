# Use the official Python slim image for a smaller footprint
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for ChromaDB / SQLite / GCC
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . ./

# Expose the port (Cloud Run defaults to 8080)
EXPOSE 8080

# Command to run the application securely via Waitress or Gunicorn
# Using gunicorn as the production WSGI server. 
# --threads ensures it can handle concurrent streaming operations.
# --timeout is extended due to intensive LLM AI agent tasks.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 300 app:app
