# app.py
from flask import Flask, render_template, jsonify
from serial_reader import start_serial_thread, get_live_count
from serial_db import get_last_20_records
from serial_reader import get_live_count,threshold


app = Flask(__name__)


start_serial_thread()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/live_count")
def api_live_count():
    count = get_live_count()
    print("[API] Live count sent to frontend:", count)
    return jsonify({"count": count})

@app.route("/api/over_threshold_records")
def over_threshold_records():
    data = get_last_20_records()
    return jsonify(data)

@app.route('/read-data')
def read_data():
    records = get_last_20_records()
    current_value = get_live_count()
    over_limit = current_value > threshold
    return jsonify({'records': records, 'over_limit': over_limit})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
