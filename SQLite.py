import sqlite3 as sq

# Установление соединения с базой данных
def init_db():
    with sq.connect('my_database.db') as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS images")
        cur.execute("""CREATE TABLE IF NOT EXISTS images (
            file_id TEXT PRIMARY KEY,
            name TEXT,
            weight INTEGER,
            format TEXT
        )""")

def save_photo(file_id: str, name: str, weight: int, format: str):
    with sq.connect('my_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO images (file_id, name, weight, format) VALUES (?, ?, ?, ?)",(file_id, name, weight, format))

        conn.commit()

