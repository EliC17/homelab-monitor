# backend/tests/conftest.py
import os
os.environ["DATABASE_URL"] = "postgresql+psycopg://monitor:devpassword123@localhost:5432/monitor_test"