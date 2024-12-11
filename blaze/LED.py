import RPi.GPIO as GPIO
import time

# Pin configuration
RED_PIN = 19
GREEN_PIN = 13
BLUE_PIN = 26

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# Set up PWM for each color
FREQ = 100  # Frequency in Hz
red_pwm = GPIO.PWM(RED_PIN, FREQ)
green_pwm = GPIO.PWM(GREEN_PIN, FREQ)
blue_pwm = GPIO.PWM(BLUE_PIN, FREQ)

# Start PWM with 0% duty cycle (LEDs off)
red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

def set_color(red, green, blue):
    """Set the color of the RGB LED.
    
    Args:
        red (int): Red intensity (0 to 100).
        green (int): Green intensity (0 to 100).
        blue (int): Blue intensity (0 to 100).
    """
    red_pwm.ChangeDutyCycle(red)
    green_pwm.ChangeDutyCycle(green)
    blue_pwm.ChangeDutyCycle(blue)

try:
    while True:
        # Example: Cycle through colors
        print("Red")
        set_color(100, 0, 0)  # Red
        time.sleep(1)
        
        print("Green")
        set_color(0, 100, 0)  # Green
        time.sleep(1)
        
        print("Blue")
        set_color(0, 0, 100)  # Blue
        time.sleep(1)
        
        print("Yellow")
        set_color(100, 100, 0)  # Yellow
        time.sleep(1)
        
        print("Cyan")
        set_color(0, 100, 100)  # Cyan
        time.sleep(1)
        
        print("Magenta")
        set_color(100, 0, 100)  # Magenta
        time.sleep(1)
        
        print("White")
        set_color(100, 100, 100)  # White
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    # Clean up GPIO
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    GPIO.cleanup()
