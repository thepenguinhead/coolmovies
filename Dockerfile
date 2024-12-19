# Use an official Python image.
FROM python:3.9-slim
 
# Install system dependencies.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*
 
# Set the working directory.
WORKDIR /app
 
# Copy the requirements file and install dependencies.
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the application code.
COPY . .
 
# Copy and set up the entrypoint script
COPY entrypoint.sh .
RUN chmod 755 entrypoint.sh
 
# Expose the port that the Flask app runs on.
EXPOSE 5000
 
# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
 
# Run the application.
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]