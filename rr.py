from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('seating.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/seats', methods=['GET'])
def get_seats():
    conn = get_db_connection()
    seats = conn.execute('SELECT * FROM Seats').fetchall()
    conn.close()
    return jsonify([dict(seat) for seat in seats])


@app.route('/book-seats', methods=['POST'])
def book_seats():
    data = request.json
    num_seats = data.get('num_seats', 0)
    if num_seats < 1 or num_seats > 7:
        return jsonify({"error": "Can only book between 1 and 7 seats"}), 400

    conn = get_db_connection()
    
 
    row_query = '''
        SELECT row, GROUP_CONCAT(seat_id) as seat_ids 
        FROM Seats 
        WHERE is_booked = 0 
        GROUP BY row 
        HAVING COUNT(seat_id) >= ? 
        ORDER BY row
    '''
    available_row = conn.execute(row_query, (num_seats,)).fetchone()

    if available_row:
        # Booking seats in a single row
        seat_ids = available_row['seat_ids'].split(',')[:num_seats]
    else:
        seat_ids = []
        nearby_seats = conn.execute('SELECT seat_id FROM Seats WHERE is_booked = 0 ORDER BY row, seat_number').fetchall()
        for seat in nearby_seats:
            if len(seat_ids) < num_seats:
                seat_ids.append(seat['seat_id'])
            else:
                break

    if len(seat_ids) < num_seats:
        conn.close()
        return jsonify({"error": "Not enough seats available"}), 400

    conn.executemany('UPDATE Seats SET is_booked = 1 WHERE seat_id = ?', [(sid,) for sid in seat_ids])
    conn.commit()
    conn.close()

    return jsonify({"booked_seats": seat_ids})

if __name__ == '__main__':
    app.run(debug=True)
