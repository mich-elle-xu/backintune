import serial
import time

# Set up the serial port
ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

while True:
    ser.write(b'Hello from Pi 1!\n')
    time.sleep(1)

