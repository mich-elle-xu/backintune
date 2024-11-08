from gpiozero import PWMOutputDevice
from time import sleep

# Define the buzzer on GPIO 17 (BCM pin 17)
buzzer = PWMOutputDevice(17)

def play_frequency(frequency):
    # Frequency range for PWM control is 0-1000 Hz (adjustable)
    buzzer.frequency = frequency
    buzzer.value = 0.5  # 50% duty cycle to produce sound
    sleep(0.5)  # Play the tone for 0.5 seconds
    buzzer.off()  # Turn off the buzzer after playing

# Example usage
play_frequency(1000)  # 1000 Hz
sleep(1)
play_frequency(500)   # 500 Hz

