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