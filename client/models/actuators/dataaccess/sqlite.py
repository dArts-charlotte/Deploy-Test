import sqlite3

def get_database_connection():
    conn = sqlite3.connect('./models/actuators/dataaccess/schedule.db')
    return conn

def load_irrigation_schedule(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT start_time, duration FROM irrigation_schedule")
    return cursor.fetchall()

def load_lighting_schedule(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT start_time, end_time FROM lighting_schedule")
    return cursor.fetchall()

def load_air_schedule(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT start_time, end_time FROM air_schedule")
    return cursor.fetchall()

def insert_irrigation_schedule_with_datetime(conn, start_datetime, duration):
    formatted_time = start_datetime.strftime("%H:%M:%S")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO irrigation_schedule (start_time, duration) VALUES (?, ?)",
        (formatted_time, duration)
    )
    conn.commit()

def insert_lighting_schedule_with_datetime(conn, start_datetime, end_datetime):
    formatted_start_time = start_datetime.strftime("%H:%M:%S")
    formatted_end_time = end_datetime.strftime("%H:%M:%S")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO lighting_schedule (start_time, end_time) VALUES (?, ?)",
        (formatted_start_time, formatted_end_time)
    )
    conn.commit()

def insert_air_schedule_with_datetime(conn, start_datetime, end_datetime):
    formatted_start_time = start_datetime.strftime("%H:%M:%S")
    formatted_end_time = end_datetime.strftime("%H:%M:%S")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO air_schedule (start_time, end_time) VALUES (?, ?)",
        (formatted_start_time, formatted_end_time)
    )
    conn.commit()

def remove_irrigation_schedule(conn, start_time):
    cursor = conn.cursor()
    print('removing irg ', start_time)
    cursor.execute(
        "DELETE FROM irrigation_schedule WHERE start_time = ?",
        (start_time)
    )
    conn.commit()

def remove_lighting_schedule(conn, start_time, end_time):
    cursor = conn.cursor()
    print('removing light ', start_time, end_time)

    cursor.execute(
        "DELETE FROM lighting_schedule WHERE start_time = ? AND end_time = ?",
        (start_time, end_time)
    )
    conn.commit()


def remove_air_schedule(conn, start_time, end_time):
    cursor = conn.cursor()
    print('removing air ', start_time, end_time)

    cursor.execute(
        "DELETE FROM air_schedule WHERE start_time = ? AND end_time = ?",
        (start_time, end_time)
    )
    conn.commit()
