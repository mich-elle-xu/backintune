import subprocess

# Path to save the video
VIDEO_PATH = "videos/video.mp4"

process = None

def start_recording():
    global process
    if process is None:
        # Example command to start video recording using ffmpeg
        command = [
            "ffmpeg",
            "-f", "v4l2",          # Video input format
            "-framerate", "30",    # Framerate
            "-video_size", "640x480", # Resolution
            "-i", "/dev/video0",   # Camera device
            VIDEO_PATH             # Output file
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Recording started.")

def stop_recording():
    global process
    if process is not None:
        process.terminate()
        process.wait()
        process = None
        print("Recording stopped.")

