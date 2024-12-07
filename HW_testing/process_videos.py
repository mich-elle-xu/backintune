import os
import subprocess

# Paths to input and output folders
input_folder = "unprocessed_videos"
output_folder = "testing_videos"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    # Process only video files
    if filename.lower().endswith(('.mp4')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # FFmpeg command to scale video and set frame rate
        command = [
            "ffmpeg",
            "-i", input_path,         # Input file
            "-vf", "scale=640:480",   # Video filter to resize
            "-r", "30",               # Set frame rate to 30 fps
            "-c:a", "copy",           # Copy audio without re-encoding
            output_path               # Output file
        ]

        print(f"Processing {filename}...")
        try:
            # Run the FFmpeg command
            subprocess.run(command, check=True)
            print(f"Processed: {filename} -> {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to process {filename}: {e}")

print("Processing complete!")
