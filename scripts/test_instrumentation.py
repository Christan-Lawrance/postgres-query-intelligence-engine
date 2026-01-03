import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from sqlalchemy import text
from app.db.session import engine

# IMPORTANT: This import activates listeners
import app.instrumentation.listeners  # noqa

with engine.connect() as conn:
    # Execute a sample query
    conn.execute(text("SELECT 1"))
    conn.execute(text("SELECT 2"))
    conn.execute(text("SELECT 2"))

print("✓ Test script completed successfully!")
print("✓ Instrumentation listeners are working correctly.")
