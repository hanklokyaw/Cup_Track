# server.py
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

db_path = "cup_track_db.db"


def add_to_cups_with_orders(tag_id, so_id, item, date=None):
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
        return "Cups with orders updated successfully."

    except sqlite3.Error as e:
        return f"Database error occurred: {e}"
    finally:
        conn.close()


@app.route('/add_order', methods=['POST'])
def add_order():
    data = request.json
    tag_id = data.get('tag_id')
    so_id = data.get('so_id')
    item = data.get('item')

    if not tag_id or not so_id or not item:
        return jsonify({"error": "Missing data"}), 400

    message = add_to_cups_with_orders(tag_id, so_id, item)
    return jsonify({"message": message}), 200


@app.route('/add_log', methods=['POST'])
def add_log():
    data = request.json
    operator_tag_id = data.get('operator_tag_id')
    tag_id = data.get('tag_id')
    device_id = data.get('device_id')
    timestamp = data.get('timestamp', datetime.now().isoformat())

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    INSERT INTO cups_logs (operator_tag_id, tag_id, device_id, timestamp)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (operator_tag_id, tag_id, device_id, timestamp))

    conn.commit()
    conn.close()

    return jsonify({"message": "Log added successfully"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5022)  # Make sure to run on an accessible IP and port
