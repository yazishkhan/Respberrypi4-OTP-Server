import serial, time

ser = serial.Serial("/dev/serial0", 9600, timeout=1)
time.sleep(2)

def at(cmd):
    ser.write((cmd + '\r\n').encode())
    time.sleep(1)
    return ser.read_all().decode(errors='ignore')

print("[AT] Basic:", at("AT"))
print("[SIM] Check:", at("AT+CPIN?"))
print("[Signal] Strength:", at("AT+CSQ"))
print("[Network] Reg:", at("AT+CREG?"))
print("[Operator]:", at("AT+COPS?"))

ser.close()

