from . import patients, pharmacies, prescriptions, schedules


def get_all(table):
    """Get all objects from the database."""
    connection = get_connection()
    cursor = connection.cursor()

    sql = f"SELECT * FROM {table};"
    cursor.execute(sql, (table))
    rows = cursor.fetchall()
    connection.close()
    column_names = [description[0] for description in cursor.description]

    return [dict(zip(column_names, row)) for row in rows]
