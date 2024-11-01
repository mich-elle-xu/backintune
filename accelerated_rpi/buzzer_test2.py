from gpiozero import PWMOutputDevice
from time import sleep

# Initialize the PWM pin for the buzzer on GPIO 18
buzzer = PWMOutputDevice(18)

# Set the maximum volume (PWM value)
max_volume = 1.0  # 100% duty cycle

try:
    while True:
        # Set a frequency (in Hz)
        frequency = 10000  # 2000 Hz is a common frequency for maximizing loudness
        
        # Set the buzzer to the maximum volume and play a tone
        buzzer.frequency = frequency
        buzzer.value = max_volume  # 100% volume
        print("Buzzer ON at {} Hz".format(frequency))
        # sleep(1)  # Play for 1 second
        
        # Turn off the buzzer
        buzzer.value = 0.0  # 0% volume
        print("Buzzer OFF")
        # sleep(1)  # Keep it off for 1 second

except KeyboardInterrupt:
    print("Exiting program")

finally:
    buzzer.close()  # Clean up when done

