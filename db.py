"""Database module for the application."""
import pickle
import random
import sqlite3

import backup


# connect to the sqlite database
def get_connection():
    """Get a connection to the database."""
    return sqlite3.connect("data.db")


# create a table in the database
def create_tables():
    """Create the tables in the migrations.sql file."""
    connection = get_connection()
    cursor = connection.cursor()

    with open("migrations.sql") as f:
        cursor.executescript(f.read())

    connection.commit()
    connection.close()


def insert(table, **kwargs):
    """Insert an object into the database."""
    kwargs["id"] = random.Random().randint(1, 1000000)
    connection = get_connection()
    cursor = connection.cursor()

    columns = ", ".join(kwargs.keys())
    values = ", ".join(["?"] * len(kwargs))

    sql = f"INSERT INTO {table} ({columns}) VALUES ({values});"
    cursor.execute(sql, tuple(kwargs.values()))

    connection.commit()
    connection.close()
    return get(table, kwargs["id"])[0]


def update(table, **kwargs):
    """Update an object in the database."""
    connection = get_connection()
    cursor = connection.cursor()

    columns = ", ".join([f"{key} = ?" for key in kwargs])
    sql = f"UPDATE {table} SET {columns} WHERE id = ?;"

    cursor.execute(sql, tuple(kwargs.values()) + (kwargs["id"],))
    connection.commit()
    connection.close()

    return get(table, kwargs["id"])[0]


def delete(table, id):

    connection = get_connection()
    cursor = connection.cursor()

    sql = f"DELETE FROM {table} WHERE id = ?;"

    cursor.execute(sql, (id,))
    connection.commit()
    connection.close()

    return True


def get(table, id):
    """Get an object from the database."""
    connection = get_connection()
    cursor = connection.cursor()

    sql = f"SELECT * FROM {table} WHERE id = ?;"
    cursor.execute(sql, (id,))
    row = cursor.fetchone()
    connection.close()

    return row


def get_all(table):
    """Get all objects from the database."""
    connection = get_connection()
    cursor = connection.cursor()

    sql = f"SELECT * FROM {table};"
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()
    column_names = [description[0] for description in cursor.description]
    rows = [dict(zip(column_names, row)) for row in rows]
    if table == "schedules":
        # the morning, afternoon, and evening columns are stored as pickled lists
        # self.morning_medication = pickle.loads(schedule["morning_medication"])
        # self.afternoon_medication = pickle.loads(schedule["afternoon_medication"])
        # self.evening_medication = pickle.loads(schedule["evening_medication"])
        # so we need to unpickle them
        for row in rows:
            if row["morning_medication"]:
                row["morning_medication"] = pickle.loads(row["morning_medication"])
            if row["afternoon_medication"]:
                row["afternoon_medication"] = pickle.loads(row["afternoon_medication"])
            if row["evening_medication"]:
                row["evening_medication"] = pickle.loads(row["evening_medication"])
    return rows


def get_prescriptions_for_patient(id):
    """get all prescriptions for a patient"""
    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT * FROM prescriptions WHERE patient_id = ?;"
    cursor.execute(sql, (id,))
    rows = cursor.fetchall()
    connection.close()

    return rows


def get_schedule_for_patient(id):
    """get all prescriptions for a patient"""
    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT * FROM schedule WHERE patient_id = ?;"
    cursor.execute(sql, (id,))
    rows = cursor.fetchall()

    connection.close()

    return rows


def get_pharmacy_for_patient(id):
    """get all prescriptions for a patient"""
    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT * FROM pharmacy WHERE patient_id = ?;"
    cursor.execute(sql, (id,))

    row = cursor.fetchone()

    connection.close()

    return row


def wipe_database():
    """Wipe the database"""
    print("Wiping database")
    print("Are you sure? (y/n)")
    if input() == "y":
        print("let's back up the database first")
        backup.create_backup()
        print("backed up database")
        print("are you still sure you want to wipe the database? (y/n)")
        if input() == "y":
            for table in ["patients", "prescriptions", "schedules", "pharmacies"]:
                try:
                    connection = get_connection()
                    cursor = connection.cursor()
                    sql = f"DELETE FROM {table};"
                    cursor.execute(sql)
                    connection.commit()
                    connection.close()
                    print(f"deleted {cursor.rowcount} rows from {table}")
                except Exception as e:
                    print(f"error deleting rows from {table}: {e}")
            print("database wiped")
        else:
            print("aborting")
    else:
        print("aborting")
