import cv2
import time
import spidev as SPI
from PIL import Image
from lib import LCD_2inch

# Initialize the SPI display
RST = 27
DC = 25
BL = 18
disp = LCD_2inch.LCD_2inch()
disp.Init()
disp.clear()
disp.bl_DutyCycle(50)

# Initialize webcam (typically 0 for the first webcam)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Define the desired display resolution (e.g., 176x220 for a typical 2-inch SPI screen)
disp_width = disp.width
disp_height = disp.height

while True:
    # Capture frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame.")
        break

    # Resize the frame to fit the display resolution
    frame_resized = cv2.resize(frame, (disp_width, disp_height))

    # Convert the frame from BGR (OpenCV default) to RGB (required by PIL)
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

    # Convert the frame to a PIL Image
    image = Image.fromarray(frame_rgb)

    # Display the image on the LCD screen
    disp.ShowImage(image)

    # Sleep for a short while to avoid maxing out the CPU
    time.sleep(0.03)  # Adjust the delay for your needs (higher = slower)

# Release the webcam and cleanup
cap.release()
disp.module_exit()

