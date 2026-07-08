#!/bin/bash
set -e
echo "Running migrations..."
alembic upgrade head
echo "Seeding targets..."
python -m app.seed
echo "Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000