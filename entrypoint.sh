#!/bin/sh
set -e

# Apply database migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Give ownership of media to the container process (optional)
chown -R www-data:www-data /app/media || true

# Execute the CMD
exec "$@"
