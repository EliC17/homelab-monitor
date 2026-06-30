# backend/tests/conftest.py
import os
os.environ["DATABASE_URL"] = "postgresql+psycopg://monitor:BirbWorld26@localhost:5432/monitor_test"