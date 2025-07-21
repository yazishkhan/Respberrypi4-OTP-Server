import serial
import time

# --------- Open serial connection to SIM800L ----
ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=1)
time.sleep(1)

def send_at(command, delay=1):
    ser.write((command + '\r').encode())
    time.sleep(delay)
    response = ser.read_all().decode(errors='ignore')
    print(f"Command: {command} → Response:\n{response}")
    return response

# Send basic test commands to module
send_at("AT")              # Should return "OK"
send_at("AT+CSQ")          # Signal quality
send_at("AT+CCID")         # SIM card number
send_at("AT+COPS?")        # Network operator
send_at("AT+CREG?")        # Network registration status

ser.close()
