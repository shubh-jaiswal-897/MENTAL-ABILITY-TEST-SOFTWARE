#!/bin/bash
echo "=== Building Mental Ability Test Software ==="

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations (gracefully handle if DB URL is not set during static build)
python manage.py migrate --noinput || true

echo "=== Build Finished Successfully ==="
