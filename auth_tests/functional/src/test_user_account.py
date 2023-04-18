import pytest
import sys

# sys.path.append("..")
from functional.settings import conn
from psycopg2.extras import DictCursor


def test_user_sugn_up():
    """Should create a new user."""
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute("SELECT * FROM auth.user")
        user = cursor.fetchone()
        assert user[1] == 'admin'
