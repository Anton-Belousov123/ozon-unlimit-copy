import psycopg2

from secrets import secret

table_name = 'oleg'
def get_code():
    conn = psycopg2.connect(
        host=secret.DATABASE_HOST,
        database=secret.DATABASE_NAME,
        user=secret.DATABASE_LOGIN,
        password=secret.DATABASE_PASSWORD,
    )
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM {table_name} WHERE stage=%s", ("Suggested",))
    record = cur.fetchone()
    conn.close()
    if not record:
        return None
    return record[0], record[1], record[11], record[3]


def update_status(article):

    conn = psycopg2.connect(
        host=secret.DATABASE_HOST,
        database=secret.DATABASE_NAME,
        user=secret.DATABASE_LOGIN,
        password=secret.DATABASE_PASSWORD,
    )
    cur = conn.cursor()

    cur.execute(f"UPDATE {table_name} SET stage=%s WHERE s_article=%s", ("Finished Ozon", str(article)))
    conn.commit()
    conn.close()