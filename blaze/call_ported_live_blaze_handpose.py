import subprocess
import signal

# Global variable to store the process
process = None

def start_record():
    global process
    process = subprocess.Popen(['python3', '/home/jessiefan/backintune/backintune/blaze/ported_live_blaze_handpose.py'])
    print("recording started!")

def stop_record():
    global process
    if process:
        # Send the SIGINT signal (Ctrl+C equivalent) to stop the process
        process.send_signal(signal.SIGINT)
        process.wait()  # Wait for the process to fully terminate
        print("recording stopped!")
    else:
        print("No running process to stop.")

