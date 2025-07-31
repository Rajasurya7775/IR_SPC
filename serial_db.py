# serial_db.py
import mysql.connector
from datetime import datetime
from pytz import timezone

india = timezone('Asia/Kolkata')

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Surya@2005',
    'database': 'sensor_data'
}

THRESHOLD = 7  # Can be changed anytime

def insert_if_threshold_exceeded(value):
    if value > THRESHOLD:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            query = "INSERT INTO data (sensor_value, timestamp) VALUES (%s, %s)"
            cursor.execute(query, (value, datetime.now(india)))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print("[DB Insert Error]", e)

def get_last_20_records():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT sensor_value, timestamp FROM data ORDER BY timestamp DESC LIMIT 20")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert timestamp to timezone-aware ISO string
        for row in rows:
            ts = row['timestamp']
            if ts.tzinfo is None:
                # Assume DB timestamp is naive, treat as UTC first or local time as you know
                # Usually DB datetime is naive and local — so attach India timezone
                ts = india.localize(ts)
            else:
                # Convert to India timezone if needed
                ts = ts.astimezone(india)
            # Format as ISO 8601 string with offset, e.g. 2025-05-25T16:26:08+05:30
            row['timestamp'] = ts.isoformat()

        return rows
    except Exception as e:
        print("[DB Fetch Error]", e)
        return []

