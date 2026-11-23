
import sqlite3
from datetime import datetime

DB_PATH = "attendance.db"


def mark_attendance(name):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            time TEXT,
            UNIQUE(name, date)
        )
    """)

    now = datetime.now()

    try:
        cursor.execute("""
            INSERT INTO attendance (name, date, time)
            VALUES (?, ?, ?)
        """, (
            name,
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S")
        ))

        conn.commit()
        result = "Attendance marked"

    except sqlite3.IntegrityError:
        result = "Already marked today"

    conn.close()

    return result
