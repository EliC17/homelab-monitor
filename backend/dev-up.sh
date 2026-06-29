#!/bin/bash
cd "$(dirname "$0")/.."
docker compose up -d db
cd backend
source .venv/Scripts/activate
uvicorn app.main:app --reload