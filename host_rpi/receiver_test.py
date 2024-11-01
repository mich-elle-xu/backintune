import serial

# Set up the serial port
ser = serial.Serial('/dev/ttyAMA10', baudrate=9600, timeout=1)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        print(f"Received: {line}")

