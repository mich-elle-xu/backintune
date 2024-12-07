import subprocess
import time
import os
import csv
import ffmpeg

# Function to get video length using moviepy
def get_video_length_ffmpeg(video_path):
    try:
        # Get video metadata using ffmpeg-python
        probe = ffmpeg.probe(video_path)
        # Extract the duration from the metadata (in seconds)
        video_length = float(probe['streams'][0]['duration'])
        return video_length
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to run your program and get processing time and average FPS
def run_program(video_path):
    # Get video length using moviepy
    video_length = get_video_length_ffmpeg(video_path)
    
    if video_length is None:
        return None, None, None
    
    # Start timing the process
    # start_time = time.perf_counter()

    # Construct the command to run your program
    command = [
        'python3', 'ported_live_blaze_handpose.py', '--vol', '0', '--input', video_path, '--display', "True"
    ]

    try:
        # Run the program and capture the output
        os.chdir('/home/jessiefan/backintune/blaze')
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        os.chdir('/home/jessiefan/backintune/HW_testing')
        
        # Capture processing time and average FPS from the output
        processing_time = 0.0
        avg_fps = 0.0
        
        for line in result.stdout.splitlines():
            if "Total processing time" in line:
                processing_time = float(line.split(":")[1].strip().split()[0])
            if "Average FPS" in line:
                avg_fps = float(line.split(":")[1].strip())

        # End timing
        # end_time = time.perf_counter()
        # processing_time = end_time - start_time  # You can use your own method for capturing the processing time
        
        return processing_time, avg_fps, video_length

    except subprocess.CalledProcessError as e:
        print(f"Error processing {video_path}: {e}")
        return None, None, None

# Function to process all videos in the folder and store results in a CSV file
def process_all_videos(folder_path, output_csv):
    # Open the CSV file for writing the results
    with open(output_csv, mode='w', newline='') as csvfile:
        fieldnames = ['Video Name', 'Processing Time (s)', 'Average FPS', 'Video Length (s)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Loop through all files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.mp4') or filename.endswith('.mov'):  # Add more formats if needed
                video_path = os.path.join(folder_path, filename)
                print(f"Processing {filename}...")

                # Run the program and get the results
                processing_time, avg_fps, video_length = run_program(video_path)

                if processing_time is not None:
                    # Write the results to the CSV
                    writer.writerow({
                        'Video Name': filename,
                        'Processing Time (s)': f"{processing_time:.2f}",
                        'Average FPS': f"{avg_fps:.2f}",
                        'Video Length (s)': f"{video_length:.2f}"
                    })
                else:
                    print(f"Skipping {filename} due to errors.")

# Example usage
folder_path = '/home/jessiefan/backintune/HW_testing/testing_videos'  # Folder containing your videos
output_csv = '/home/jessiefan/backintune/HW_testing/video_processing_results.csv'  # Output CSV file

process_all_videos(folder_path, output_csv)
