import sqlite3
from datetime import datetime

db_path = "cup_track_db.db"

### v2
def add_to_cups_with_orders(db_path, tag_id, so_id, item, date=None):
    if date is None:
        date = datetime.now().date()  # Use current date if not provided

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if tag_id exists in cups table
        cursor.execute("SELECT id FROM cups WHERE tag_id = ?", (tag_id,))
        if not cursor.fetchone():  # If tag_id does not exist
            cursor.execute("INSERT INTO cups (tag_id) VALUES (?);", (tag_id,))

        # Check if so_id exists in sales_orders table
        cursor.execute("SELECT id FROM sales_orders WHERE so_id = ?", (so_id,))
        if not cursor.fetchone():  # If so_id does not exist
            cursor.execute("INSERT INTO sales_orders (so_id) VALUES (?);", (so_id,))

        # Check if the item exists in the items table
        cursor.execute("SELECT id FROM items WHERE item = ?", (item,))
        if not cursor.fetchone():  # If item does not exist
            cursor.execute("INSERT INTO items (item) VALUES (?);", (item,))

        # Now insert into cups_with_orders
        query = """
        INSERT INTO cups_with_orders (tag_id, so_id, item, date)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (tag_id, so_id, item, date))

        conn.commit()
        print("Cups with orders updated successfully.")

    except sqlite3.Error as e:
        print("Database error occurred:", e)
    finally:
        conn.close()


def add_to_cups_logs(db_path, operator_tag_id, cup_tag_id, device_id, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()  # Use current time if not provided

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    INSERT INTO cups_logs (operator_tag_id, tag_id, device_id, timestamp)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (operator_tag_id, cup_tag_id, device_id, timestamp))

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


def add_sales_order(db_path, so_id):
    """
    Inserts a new sales order with the specified so_id into the sales_orders table.

    Parameters:
        db_path (str): The path to the SQLite database.
        so_id (int): The sales order ID to add.

    Returns:
        int: The ID of the newly inserted sales order, or None if the insertion fails.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        query = "INSERT INTO sales_orders (so_id) VALUES (?);"
        cursor.execute(query, (so_id,))
        conn.commit()

        # Get the last inserted id (id of the newly added sales order)
        new_id = cursor.lastrowid
    except sqlite3.Error as e:
        print("Error occurred:", e)
        new_id = None
    finally:
        conn.close()

    return new_id

# # Assuming cup_track.db is in the same directory as server.py
# new_cup_id = add_cup(db_path, "TAG001")
#
# if new_cup_id:
#     print(f"New cup added with ID: {new_cup_id}")
# else:
#     print("Failed to add cup.")
#
#
#
# # Assuming cup_track.db is in the same directory as server.py
# new_sales_order_id = add_sales_order(db_path, 101569213)
#
# if new_sales_order_id:
#     print(f"New sales order added with ID: {new_sales_order_id}")
# else:
#     print("Failed to add sales order.")


# Assuming cup_track.db is in the same directory as server.py
add_to_cups_with_orders("cup_track_db.db", "TAG002", 101578181, "ED-PRGEFAC-TI-25g-2")  # Assuming item_id = 1 exists
