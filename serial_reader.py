# serial_reader.py
import serial
import threading
from serial_db import insert_if_threshold_exceeded
from email_alert import send_threshold_alert  # We’ll define this

PORT = "COM4"
BAUD_RATE = 9600

_live_count = 0 # Private variable
threshold = 7

# Place this as a global or persistent variable
was_above_threshold = False
email_sent = False  # To prevent multiple emails


def handle_sensor_value(value):
    global was_above_threshold,email_sent

    if value > threshold and not was_above_threshold:
        # Value just crossed above threshold
        was_above_threshold = True
        insert_if_threshold_exceeded(value)  # Call your insert function here

        if not email_sent:
            send_threshold_alert(value)  # ✅ Send email here
            email_sent = True
    elif value < threshold:
        was_above_threshold = False  # Reset so it can trigger again later
        email_sent = False  # Reset when it drops back below threshold


def get_live_count():
    return _live_count

def read_serial():
    global _live_count
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
        print(f"[Serial Thread] Opened port {PORT}")
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"[Serial Thread] Received line: {line}")
                if "Count:" in line:
                    count_str = line.split("Count:")[-1].strip()
                    if count_str.lstrip('-').isdigit():  # allow negative sign if needed
                        _live_count = int(count_str)
                        print(f"Live Count Updated: {_live_count}")

                        handle_sensor_value(_live_count)
    except Exception as e:
        print(f"[Serial Error] {e}")

def start_serial_thread():
    print("[Serial Thread] Starting serial read thread...")
    t = threading.Thread(target=read_serial, daemon=True)
    t.start()

