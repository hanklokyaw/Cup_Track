import sqlite3
from datetime import datetime


def add_to_cups_with_orders(db_path, tag_id, so_id, item_id, date=None):
    if date is None:
        date = datetime.now().date()  # Use current date if not provided

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    INSERT INTO cups_with_orders (tag_id, so_id, item_id, date)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (tag_id, so_id, item_id, date))

    conn.commit()
    conn.close()


def add_to_cups_logs(db_path, operator_id, tag_id, device_id, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()  # Use current time if not provided

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    INSERT INTO cups_logs (operator_id, tag_id, device_id, timestamp)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (operator_id, tag_id, device_id, timestamp))

    conn.commit()
    conn.close()


def add_cup(db_path, tag_id):
    """
    Inserts a new cup with the specified tag_id into the cups table.

    Parameters:
        db_path (str): The path to the SQLite database.
        tag_id (str): The tag ID of the cup to add.

    Returns:
        int: The ID of the newly inserted cup, or None if the insertion fails.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        query = "INSERT INTO cups (tag_id) VALUES (?);"
        cursor.execute(query, (tag_id,))
        conn.commit()

        # Get the last inserted id (id of the newly added cup)
        new_id = cursor.lastrowid
    except sqlite3.Error as e:
        print("Error occurred:", e)
        new_id = None
    finally:
        conn.close()

    return new_id

