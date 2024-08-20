import sqlite3

def create_tables():
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()

    # Create irrigation_schedule table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS irrigation_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT NOT NULL,
            duration INTEGER NOT NULL
        )
    ''')


    # Create lighting_schedule table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lighting_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
    ''')

    # Create air_schedule table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS air_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
