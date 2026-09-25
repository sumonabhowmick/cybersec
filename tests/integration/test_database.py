"""Database integration tests are opt-in through an explicitly configured test database."""
import os
import pytest

@pytest.mark.skipif(os.getenv("RUN_DATABASE_TESTS")!="1",reason="Set RUN_DATABASE_TESTS=1 with a disposable configured PostgreSQL database")
def test_database_connectivity():
    from src.database.connection import connect
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            assert cursor.fetchone()[0]==1
