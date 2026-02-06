from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder='Weekend_Trip/web')

DB_PATH = os.path.join(os.path.dirname(__file__), 'Weekend_Trip', 'database', 'trip_data.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Serve Frontend Files
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# API Endpoints
@app.route('/api/itinerary', methods=['GET'])
def get_itinerary():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM itinerary ORDER BY day_number, id').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in items])

@app.route('/api/itinerary', methods=['POST'])
def add_itinerary():
    new_item = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO itinerary (day_number, time_slot, activity_title, activity_description, category) VALUES (?, ?, ?, ?, ?)',
                 (new_item['day_number'], new_item['time_slot'], new_item['activity_title'], new_item['activity_description'], new_item['category']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 201

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM expenses ORDER BY date DESC').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in items])

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    new_item = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO expenses (category, amount, description, date) VALUES (?, ?, ?, ?)',
                 (new_item['category'], new_item['amount'], new_item['description'], new_item['date']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 201

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in items])

@app.route('/api/menu', methods=['GET'])
def get_menu():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM menu').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in items])

@app.route('/api/menu', methods=['POST'])
def add_menu_item():
    new_item = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO menu (name, description, price, image_url, category) VALUES (?, ?, ?, ?, ?)',
                 (new_item['name'], new_item['description'], new_item['price'], new_item['image_url'], new_item['category']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 201

@app.route('/api/orders', methods=['GET', 'POST'])
def handle_orders():
    conn = get_db_connection()
    if request.method == 'POST':
        new_order = request.json
        conn.execute('INSERT INTO food_orders (item_name, quantity, total_price, payment_method, seating_info) VALUES (?, ?, ?, ?, ?)',
                     (new_order['item_name'], new_order.get('quantity', 1), new_order['total_price'], new_order['payment_method'], new_order.get('seating_info', 'Walk-in')))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 201
    else:
        items = conn.execute('SELECT * FROM food_orders ORDER BY timestamp DESC').fetchall()
        conn.close()
        return jsonify([dict(ix) for ix in items])

@app.route('/api/hosts', methods=['GET'])
def get_hosts():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM host_info').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in items])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
