import smtplib
from email.mime.text import MIMEText

def send_threshold_alert(value):
    sender_email = "################"
    receiver_email = "####################"
    subject = "Alert: Sensor Value Threshold Crossed"
    body = f"The sensor value has exceeded the threshold! Current value: {value}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, "reej cwim ermr mdcs")  # Use app password if using Gmail
            server.send_message(msg)
            print("[Email Sent] Threshold alert sent.")
    except Exception as e:
        print(f"[Email Error] {e}")
