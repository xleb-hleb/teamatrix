#!/bin/bash
set -e

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"

echo "Waiting for database at $DB_HOST:$DB_PORT..."
while ! python -c "
import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('$DB_HOST', $DB_PORT))
    s.close()
except Exception:
    sys.exit(1)
" 2>/dev/null; do
    sleep 1
done
echo "Database is ready!"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn teamatrix.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
