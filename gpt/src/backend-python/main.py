# file: backend-python/main.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)
# Enable CORS to allow requests from the React frontend
CORS(app)

# Function to get a database connection
def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn

@app.route('/api/python/increment', methods=['POST'])
def increment_python_count():
    """Increments the python request count in the database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Atomically increment the python count and update the timestamp
        query = """
            UPDATE request_counts
            SET python_requested_counts = python_requested_counts + 1,
                last_python_request_time = %s
            WHERE id = 1
        """
        cur.execute(query, (datetime.now(),))
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({"message": "Python count incremented successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to increment Python count"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
