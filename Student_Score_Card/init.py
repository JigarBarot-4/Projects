from database import get_connection

def create_table():
    conn = get_connection()     # connect to sqllite3
    cursor = conn.cursor()      # excecute sql queries

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY NOT NULL,
        name TEXT NOT NULL,
        class INT NOT NULL,
        marks INT NOT NULL
        )"""
    )
    conn.commit()
    conn.close()

#insert data 
def insert_data():
    conn = get_connection()     # connect to sqllite3
    cursor = conn.cursor()      # excecute sql queries

    students = [
        ("student1","John Doe", 10, 85),
        ("student2","Jane Smith", 9, 92),
        ("student3","Michael Johnson", 11, 78),
        ("student4","Emily Davis", 10, 95),
        ("student5","William Brown", 12, 88)
    ]

    cursor.executemany(
    """INSERT OR REPLACE INTO students (student_id, name, class, marks) VALUES (?, ?, ?, ?)""", students)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    insert_data()
    print("Table created and data inserted successfully.")