#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is up."

# Run database migrations
echo "Applying database migrations..."
flask db upgrade

# Import data if not already imported
if [ ! -f /app/imported ]; then
    echo "Importing data from top_media.csv..."
    python /app/src/import_data.py /app/src/data/top_media.csv
    touch /app/imported
else
    echo "Data already imported."
fi

# Start the Flask application
exec "$@"