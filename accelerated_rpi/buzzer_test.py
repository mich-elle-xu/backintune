import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the buzzer pin
buzzer_pin = 18
GPIO.setup(buzzer_pin, GPIO.OUT)

try:
    while True:
        # Turn the buzzer on
        GPIO.output(buzzer_pin, GPIO.HIGH)
        print("Buzzer ON")
        time.sleep(1)  # Keep it on for 1 second
        
        # Turn the buzzer off
        GPIO.output(buzzer_pin, GPIO.LOW)
        print("Buzzer OFF")
        time.sleep(1)  # Keep it off for 1 second

except KeyboardInterrupt:
    print("Exiting program")

finally:
    # Clean up GPIO settings
    GPIO.cleanup()
