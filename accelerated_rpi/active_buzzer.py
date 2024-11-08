from gpiozero import Buzzer
from time import sleep

# Set up buzzer on GPIO pin 17 (physical pin 11)
buzzer = Buzzer(17)

# Turn the buzzer on and off with a delay
while True:
    buzzer.on()  # Turn the buzzer on
    sleep(1)     # Wait for 1 second
    buzzer.off() # Turn the buzzer off
    sleep(1)     # Wait for 1 second

