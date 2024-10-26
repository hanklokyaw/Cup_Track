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


# Function to get operator information
def get_operator_info_from_db(operator_tag_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM operators WHERE tag = ?", (operator_tag_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]  # Return operator name
    else:
        return None

# Function to get sales order information
def get_so_info_from_db(cup_tag_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT so_id FROM cups_with_orders WHERE tag_id = ?", (cup_tag_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]  # Return sales order ID
    else:
        return None

# Flask route for getting operator information
@app.route('/get_operator/<operator_tag_id>', methods=['GET'])
def get_operator(operator_tag_id):
    operator_name = get_operator_info_from_db(operator_tag_id)
    if operator_name:
        return jsonify({"operator_name": operator_name}), 200
    else:
        return jsonify({"error": "Operator not found"}), 404

# Flask route for getting sales order information
@app.route('/get_so/<cup_tag_id>', methods=['GET'])
def get_sales_order(cup_tag_id):
    sales_order_id = get_so_info_from_db(cup_tag_id)
    if sales_order_id:
        return jsonify({"sales_order_id": sales_order_id}), 200
    else:
        return jsonify({"error": "Sales order not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5022)  # Make sure to run on an accessible IP and port
