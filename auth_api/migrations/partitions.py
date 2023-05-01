import psycopg2
from core.config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB


def create_partition():
    """ creating partition by user_sign_in """
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB
    )
    with conn.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS "user_login_history_2" PARTITION OF auth.user_login_history
            FOR VALUES FROM ('2023-05-01') TO ('2023-07-01');
            """
        )
    conn.commit()
    conn.close()
