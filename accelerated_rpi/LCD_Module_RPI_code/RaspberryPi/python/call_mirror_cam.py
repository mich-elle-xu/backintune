import subprocess
import os
import signal
import time

# Global variable to store the process
process = None

def start_mirror_cam():
    global process
    # Start mirror_cam.py with sudo (ensure sudoers allow passwordless execution)
    process = subprocess.Popen(['sudo', 'python3', '/home/jessiefan/backintune/accelerated_rpi/LCD_Module_RPI_code/RaspberryPi/python/mirror_cam.py'])
    print("mirror_cam.py started!")

def stop_mirror_cam():
    global process
    if process:
        # Send the SIGINT signal (Ctrl+C equivalent) to stop the process
        process.send_signal(signal.SIGINT)
        process.wait()  # Wait for the process to fully terminate
        print("mirror_cam.py stopped!")
    else:
        print("No running process to stop.")

