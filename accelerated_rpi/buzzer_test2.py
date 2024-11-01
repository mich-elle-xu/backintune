from gpiozero import Buzzer
from time import sleep

# Initialize the buzzer on GPIO 18
buzzer = Buzzer(18)

try:
    while True:
        buzzer.on()  # Turn on the buzzer
        print("Buzzer ON")
        sleep(1)     # Keep it on for 1 second
        
        buzzer.off()  # Turn off the buzzer
        print("Buzzer OFF")
        sleep(1)     # Keep it off for 1 second

except KeyboardInterrupt:
    print("Exiting program")

