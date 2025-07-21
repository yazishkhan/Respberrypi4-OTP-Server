from flask import Flask, request, jsonify
import serial
import time
import random

app = Flask(__name__)

def send_sms(number, message):
    try:
        sim800 = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
        time.sleep(1)

        sim800.write(b'AT\r')
        time.sleep(0.5)
        sim800.write(b'AT+CMGF=1\r')  # SMS text mode
        time.sleep(0.5)
        sim800.write(f'AT+CMGS="{number}"\r'.encode())
        time.sleep(0.5)
        sim800.write(f'{message}\x1A'.encode())   
        time.sleep(3)

        sim800.close()
        return True
    except Exception as e:
        print("Error sending SMS:", e)
        return False

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    phone = data.get("phone")

    if not phone:
        return jsonify({"error": "Phone number required"}), 400

    otp = str(random.randint(100000, 999999))
    message = f"Your OTP is {otp}"

    success = send_sms(phone, message)

    if success:
        return jsonify({"status": "OTP sent successfully!"})  # Dosn’t return OTP in real case this condition  is to indicate the status 
    else:
        return jsonify({"error": "Failed to send SMS"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
