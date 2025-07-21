from flask import Flask, request, jsonify
import random
import time
import pymysql
from datetime import datetime, timedelta
import serial

app = Flask(__name__)

# -------------------------- SIM800L Serial Setup ------------------------------------------------
ser = serial.Serial("/dev/serial0", 9600, timeout=1)
time.sleep(1)

# ---------------- MySQL Setup ---------------------------------------
db = pymysql.connect(
    host="localhost",
    user="root",
    password="741593",  # Replace this password if you give diff password while seetingup the SQL
    database="otp_service"
)
cursor = db.cursor()

# ------------------------ Send SMS -----------------
def send_sms(phone, otp):
    ser.write(b'AT+CMGF=1\r')  # Set text mode
    time.sleep(0.5)
    ser.write(f'AT+CMGS="{phone}"\r'.encode())
    time.sleep(0.5)
    ser.write(f'Your OTP i {otp}\x1A'.encode()) 
    time.sleep(3)

# ------------- Auto-delete expired OTPs --------------------
def delete_expired_otps():
    cursor.execute("DELETE FROM otps WHERE created_at < NOW() - INTERVAL 10 MINUTE")
    db.commit()

# -------------------------------- Send OTP Endpoint -------------------
@app.route('/send_otp', methods=['POST'])
def send_otp():
    phone = request.json.get("phone")
    otp = str(random.randint(100000, 999999))

    try:
        # Send SMS 
        send_sms(phone, otp)

        # Clean old OTPs
        delete_expired_otps()

        # Store in DB
        cursor.execute("INSERT INTO otps (phone, otp) VALUES (%s, %s)", (phone, otp))
        db.commit()

        return jsonify({"status": "OTP sent successfully !! Dev by Yazish Khan"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------- Verify OTP Endpoint --------------------
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    phone = request.json.get("phone")
    user_otp = request.json.get("otp")

    # Clean old OTPs first
    delete_expired_otps()

    cursor.execute("""
        SELECT otp, created_at FROM otps 
        WHERE phone = %s 
        ORDER BY created_at DESC LIMIT 1
    """, (phone,))
    result = cursor.fetchone()

    if not result:
        return jsonify({"valid": False, "error": "No OTP found"})

    db_otp, created_at = result
    now = datetime.now()

    if now - created_at > timedelta(minutes=10):
        return jsonify({"valid": False, "error": "OTP expired"})

    if db_otp == user_otp:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False, "error": "OTP incorrect"})

# ----- it is an optional page called Health Check ---------- 
@app.route('/health')
def health():
    return jsonify({"status": "SIM800L OK"})

# --------- Start Flask App ---------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
