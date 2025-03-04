import sqlite3 as sq

# Установление соединения с базой данных
with sq.connect('my_database.db') as conn:
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS images")
    cur.execute("""CREATE TABLE IF NOT EXISTS images (
        file_id TEXT PRIMARY KEY,
        name TEXT,
        weight INTEGER,
        format TEXT
    )""")