



TO RUN, bash dev-up.sh
TO STOP, CTRL+C, bash dev-down.sh

In seperate terminal run source .venv/Scripts/activate

For testing once in .venv run these
docker exec -it homelab-monitor-db-1 psql -U monitor -d monitor -c "CREATE DATABASE monitor_test;"
DATABASE_URL=postgresql+psycopg://monitor:<your-actual-password>@localhost:5432/monitor_test alembic upgrade head
pytest
