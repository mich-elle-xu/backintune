import time
from record_video import start_recording, stop_recording

def test_video_recording():
    try:
        print("Starting video recording...")
        start_recording()  # Start the recording
        print("Recording... (wait for 5 seconds)")
        time.sleep(5)  # Record for 5 seconds
    except Exception as e:
        print(f"Error starting recording: {e}")
    finally:
        print("Stopping video recording...")
        stop_recording()  # Stop the recording
        print("Recording stopped. Check the output file.")

if __name__ == "__main__":
    test_video_recording()

