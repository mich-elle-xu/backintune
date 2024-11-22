'''
Copyright 2024 Avnet Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
#
# Blaze Demo Application (live with USB camera)
#
# References:
#   https://www.github.com/AlbertaBeef/blaze_app_python
#   https://www.github.com/AlbertaBeef/blaze_tutorial/tree/2023.1
#
# Dependencies:
#   TFLite
#      tensorflow
#    or
#      tflite_runtime
#   PyTorch
#      torch
#   Vitis-AI 3.5
#      xir
#      vitis_ai_library
#   Hailo
#      hailo_platform
#   plots
#      pyplotly
#      kaleido
#


import numpy as np
import cv2
import os
from datetime import datetime
import itertools

from ctypes import *
from typing import List
import pathlib
import threading
import time
import sys
import argparse
import glob
import subprocess
import re
import sys

from datetime import datetime
import plotly.graph_objects as go

from hand_info import Hand

import getpass
import socket
# from threading import Thread

from gpiozero import PWMOutputDevice
# Define the buzzer on GPIO 17 (BCM pin 17)
buzzer = PWMOutputDevice(17)

# TODO: set these values with web app
buzz_val = 0.2
bViewOutput = True
time_btwn_buzz = 2

tension = False

def buzz_per_sec():
    if tension:
        play_frequency(1000)
        buzz_thread = threading.Timer(time_btwn_buzz,buzz_per_sec)
        buzz_thread.daemon = True
        buzz_thread.start()
    else:
        return

def set_buzzer():
    global buzz_en
    buzz_en = True

def play_frequency(frequency):
    print("BUZZ")
    # Frequency range for PWM control is 0-1000 Hz (adjustable)
    buzzer.frequency = frequency
    buzzer.value = buzz_val
    time.sleep(0.1)  # Play the tone for 0.25 seconds
    buzzer.off()  # Turn off the buzzer after playing

user = getpass.getuser()
host = socket.gethostname()
user_host_descriptor = user+"@"+host
print("[INFO] user@hosthame : ",user_host_descriptor)

sys.path.append(os.path.abspath('blaze_common/'))
sys.path.append(os.path.abspath('blaze_tflite/'))
sys.path.append(os.path.abspath('blaze_pytorch/'))
sys.path.append(os.path.abspath('blaze_vitisai/'))
sys.path.append(os.path.abspath('blaze_hailo/'))

# TODO: figure out how to put 2 hands
right_hand = Hand(10, "right")
left_hand = Hand(10, "left")

blaze_hailo_supported = False
try:
    from blaze_hailo.hailo_inference import HailoInference
    hailo_infer = HailoInference()
    from blaze_hailo.blazedetector import BlazeDetector as BlazeDetector_hailo
    from blaze_hailo.blazelandmark import BlazeLandmark as BlazeLandmark_hailo
    print("[INFO] blaze_hailo supported ...")
    blaze_hailo_supported = True
except:
    print("[INFO] blaze_hailo NOT supported ...")

from visualization import draw_detections, draw_landmarks, draw_roi
from visualization import HAND_CONNECTIONS, FACE_CONNECTIONS, POSE_FULL_BODY_CONNECTIONS, POSE_UPPER_BODY_CONNECTIONS

from timeit import default_timer as timer

def get_media_dev_by_name(src):
    devices = glob.glob("/dev/media*")
    for dev in sorted(devices):
        proc = subprocess.run(['media-ctl','-d',dev,'-p'], capture_output=True, encoding='utf8')
        for line in proc.stdout.splitlines():
            if src in line:
                return dev

def get_video_dev_by_name(src):
    devices = glob.glob("/dev/video*")
    for dev in sorted(devices):
        proc = subprocess.run(['v4l2-ctl','-d',dev,'-D'], capture_output=True, encoding='utf8')
        for line in proc.stdout.splitlines():
            if src in line:
                return dev


# Parameters (tweaked for video)
scale = 1.0
text_fontType = cv2.FONT_HERSHEY_SIMPLEX
text_fontSize = 0.75*scale
text_color    = (0,0,255)
text_lineSize = max( 1, int(2*scale) )
text_lineType = cv2.LINE_AA

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input'      , type=str, default="", help="Video input device. Default is auto-detect (first usbcam)")
ap.add_argument('-d', '--debug'      , default=False, action='store_true', help="Enable Debug mode. Default is off")
# ap.add_argument('-w', '--withoutview', default=False, action='store_true', help="Disable Output viewing. Default is on")
ap.add_argument('-f', '--fps'        , default=False, action='store_true', help="Enable FPS display. Default is off")

args = ap.parse_args()  
  
print('Command line options:')
print(' --input       : ', args.input)
print(' --debug       : ', args.debug)
print(' --fps         : ', args.fps)


blaze_pipelines = {}
blaze_pipelines["blaze"] = "hand"
blaze_pipelines["pipeline"] = "hai_hand_v0_10_lite"
blaze_pipelines["model1"] = "blaze_hailo/models/palm_detection_lite.hef"
blaze_pipelines["model2"] = "blaze_hailo/models/hand_landmark_lite.hef"

bInputImage = False
bInputVideo = False
bInputCamera = True

if os.path.exists(args.input):
    print("[INFO] Input exists : ",args.input)
    file_name, file_extension = os.path.splitext(args.input)
    file_extension = file_extension.lower()
    print("[INFO] Input type : ",file_extension)
    if file_extension == ".jpg" or file_extension == ".png" or file_extension == ".tif":
        bInputImage = True
        bInputVideo = False
        bInputCamera = False
    if file_extension == ".mov" or file_extension == ".mp4":
        bInputImage = False
        bInputVideo = True
        bInputCamera = False

if bInputVideo == True:
    # Open video file
    cap = cv2.VideoCapture(args.input)
    frame_width = int(round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    frame_height = int(round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("[INFO] input : video ",args.input," (",frame_width,",",frame_height,")")

if bInputImage == True:
    image = cv2.imread(args.input)
    frame_height,frame_width,_ = image.shape
    print("[INFO] input : image ",args.input," (",frame_width,",",frame_height,")")

if bInputCamera == True:
    print("[INFO] Searching for USB camera ...")
    dev_video = get_video_dev_by_name("uvcvideo")
    dev_media = get_media_dev_by_name("uvcvideo")
    print(dev_video)
    print(dev_media)

    if dev_video == None:
        input_video = 0
    elif args.input != "":
        input_video = args.input 
    else:
        input_video = dev_video  

    # Open video
    cap = cv2.VideoCapture(input_video)
    frame_width = 640
    frame_height = 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,frame_height)
    print("[INFO] input : camera",input_video," (",frame_width,",",frame_height,")")

output_dir = './captured-images'

profile_csv = './blaze_detect_live.csv'
if os.path.isfile(profile_csv):
    f_profile_csv = open(profile_csv, "a")
    print("[INFO] Appending to existing profiling results file :",profile_csv)
else:
    f_profile_csv = open(profile_csv, "w")
    print("[INFO] Creating new profiling results file :",profile_csv)
    f_profile_csv.write("time,user,hostname,pipeline,resize,detector_pre,detector_model,detector_post,extract_roi,landmark_pre,landmark_model,landmark_post,annotate,total,fps\n")

if not os.path.exists(output_dir):      
    os.mkdir(output_dir)            # Create the output directory if it doesn't already exist


nb_active_pipelines = 0
pipeline = blaze_pipelines["pipeline"]
model1   = blaze_pipelines["model1"]
model2   = blaze_pipelines["model2"]

blaze_pipelines["supported"] = False # until proven otherwise
blaze_pipelines["selected"] = False # until proven otherwise

blaze_pipelines["selected"] = True
if args.debug:
    print("[blaze_detect_live] Pipeline ",pipeline," selected.")

if blaze_hailo_supported and blaze_pipelines["selected"] == True:
    detector_type = "blazepalm"
    landmark_type = "blazehandlandmark"

    blaze_detector = BlazeDetector_hailo(detector_type,hailo_infer)
    blaze_detector.set_debug(debug=args.debug)
    blaze_detector.display_scores(debug=False)
    blaze_detector.load_model(model1)

    blaze_landmark = BlazeLandmark_hailo(landmark_type,hailo_infer)
    blaze_landmark.set_debug(debug=args.debug)
    blaze_landmark.load_model(model2)
    
    blaze_pipelines["supported"]     = True
    blaze_pipelines["detector_type"] = detector_type
    blaze_pipelines["detector"]      = blaze_detector
    blaze_pipelines["landmark_type"] = landmark_type
    blaze_pipelines["landmark"]      = blaze_landmark

    if args.debug:
        print("[blaze_detect_live] Pipeline ",pipeline," supported and initialized.")

    nb_active_pipelines += 1
        
if nb_active_pipelines == 0:
    print("[ERROR] no pipelines selected !")
    exit()        
        
print("================================================================")
print("Blaze Detect Live Demo")
print("================================================================")

bShowDebugImage = False

bShowFPS = True

def ignore(x):
    pass

if blaze_pipelines["supported"] and blaze_pipelines["selected"]:

    blaze_detector_type = blaze_pipelines["detector_type"]
    blaze_landmark_type = blaze_pipelines["landmark_type"]
    blaze_title = blaze_pipelines["pipeline"]
            
    app_main_title = blaze_title+" Demo"
    app_ctrl_title = blaze_title+" Demo"
    
    if bViewOutput:
        cv2.namedWindow(app_main_title)

        thresh_min_score = blaze_detector.min_score_thresh
        thresh_min_score_prev = thresh_min_score
        cv2.createTrackbar('threshMinScore', app_ctrl_title, int(thresh_min_score*100), 100, ignore)

image = []
output = []

frame_count = 0

# init the real-time FPS counter
rt_fps_count = 0
rt_fps_time = cv2.getTickCount()
rt_fps_valid = False
rt_fps = 0.0
rt_fps_message = "FPS: {0:.2f}".format(rt_fps)
rt_fps_x = int(10*scale)
rt_fps_y = int((frame_height-10)*scale)

frames = []

try:
    while True:
        # init the real-time FPS counter
        if rt_fps_count == 0:
            rt_fps_time = cv2.getTickCount()

        frame_count = frame_count + 1

        flag, frame = cap.read()
        if not flag:
            print("[ERROR] cap.read() FAILEd !")
            break

        if blaze_pipelines["supported"] and blaze_pipelines["selected"]:

            image = frame.copy()
            
            blaze_detector_type = blaze_pipelines["detector_type"]
            blaze_landmark_type = blaze_pipelines["landmark_type"]
            blaze_title = blaze_pipelines["pipeline"]
            blaze_detector = blaze_pipelines["detector"]
            blaze_landmark = blaze_pipelines["landmark"]
            
            app_main_title = blaze_title+" Demo"
            app_ctrl_title = blaze_title+" Demo"
            app_debug_title = blaze_title+" Debug"
            
            # Get trackbar values
            if bViewOutput:
                thresh_min_score = cv2.getTrackbarPos('threshMinScore', app_ctrl_title)
                if thresh_min_score < 10:
                    thresh_min_score = 10
                    cv2.setTrackbarPos('threshMinScore', app_ctrl_title,thresh_min_score)
                thresh_min_score = thresh_min_score*(1/100)
                if thresh_min_score != thresh_min_score_prev:
                    blaze_detector.min_score_thresh = thresh_min_score
                    thresh_min_score_prev = thresh_min_score
                
                
            #image = cv2.resize(image,(0,0), fx=scale, fy=scale) 
            output = image.copy()
            
            # BlazePalm pipeline
            
            start = timer()
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            img1,scale1,pad1=blaze_detector.resize_pad(image)
            profile_resize = timer()-start

            if bShowDebugImage:
                # show the resized input image
                debug_img = img1.astype(np.float32)/255.0
                debug_img = cv2.resize(debug_img,(blaze_landmark.resolution,blaze_landmark.resolution))
            
            normalized_detections = blaze_detector.predict_on_image(img1)
            if len(normalized_detections) > 0:

                start = timer()          
                detections = blaze_detector.denormalize_detections(normalized_detections,scale1,pad1)
                    
                xc,yc,scale,theta = blaze_detector.detection2roi(detections)
                roi_img,roi_affine,roi_box = blaze_landmark.extract_roi(image,xc,yc,theta,scale)
                profile_extract = timer()-start

                flags, normalized_landmarks = blaze_landmark.predict(roi_img)
                # print(flags, normalized_landmarks)
                
                if bShowDebugImage:
                    # show the ROIs
                    for i in range(roi_img.shape[0]):
                        #roi_landmarks = np.expand_dims(normalized_landmarks[i,:,:].copy(), axis=0)
                        roi_landmarks = normalized_landmarks[i,:,:].copy()
                        roi_landmarks = roi_landmarks*blaze_landmark.resolution
                        if blaze_landmark_type == "blazehandlandmark":
                            draw_landmarks(roi_img[i], roi_landmarks[:,:2], HAND_CONNECTIONS, size=2)
                        elif blaze_landmark_type == "blazefacelandmark":
                            draw_landmarks(roi_img[i], roi_landmarks[:,:2], FACE_CONNECTIONS, size=1)                                    
                        elif blaze_landmark_type == "blazeposelandmark":
                            if roi_landmarks.shape[1] > 33:
                                draw_landmarks(roi_img[i], roi_landmarks[:,:2], POSE_FULL_BODY_CONNECTIONS, size=2)
                            else:
                                draw_landmarks(roi_img[i], roi_landmarks[:,:2], POSE_UPPER_BODY_CONNECTIONS, size=2)                
                        debug_img = cv2.hconcat([debug_img,roi_img[i]])

                start = timer() 
                landmarks = blaze_landmark.denormalize_landmarks(normalized_landmarks, roi_affine)

                for i in range(len(flags)):
                    landmark, flag = landmarks[i], flags[i]
                    #if True: #flag>.5:
                    if blaze_landmark_type == "blazehandlandmark":
                        draw_landmarks(output, landmark[:,:2], HAND_CONNECTIONS, size=2)
                        wrist_pos = np.array(landmark[0, :2])
                        middle_finger_pos = np.array(landmark[9, :2])
                        cur_vector = np.subtract(middle_finger_pos, wrist_pos)
                        if (i == 0): 
                            right_hand.add_angle(right_hand.angle_between_vectors_np(cur_vector))
                            right_hand.update_tension_states()
                            right_hand.update_tension()
                        else:
                            left_hand.add_angle(left_hand.angle_between_vectors_np(cur_vector))
                    elif blaze_landmark_type == "blazefacelandmark":
                        draw_landmarks(output, landmark[:,:2], FACE_CONNECTIONS, size=1)                                    
                    elif blaze_landmark_type == "blazeposelandmark":
                        if landmarks.shape[1] > 33:
                            draw_landmarks(output, landmark[:,:2], POSE_FULL_BODY_CONNECTIONS, size=2)
                        else:
                            draw_landmarks(output, landmark[:,:2], POSE_UPPER_BODY_CONNECTIONS, size=2)                
                    
                if right_hand.tense and not tension:
                    print("TENSE")
                    play_frequency(1000)
                    tension = True
                    buzz_thread = threading.Timer(time_btwn_buzz, buzz_per_sec)
                    buzz_thread.daemon = True  # Make it a daemon thread
                    buzz_thread.start()
                elif not right_hand.tense and tension:
                    print("NOT TENSE")
                    tension = False

                draw_roi(output,roi_box)
                draw_detections(output,detections)
                profile_annotate = timer()-start

            if bShowDebugImage:
                if debug_img.shape[0] == debug_img.shape[1]:
                    zero_img = np.full_like(debug_img,0.0)
                    debug_img = cv2.hconcat([debug_img,zero_img])
                debug_img = cv2.cvtColor(debug_img,cv2.COLOR_RGB2BGR)
                cv2.imshow(app_debug_title, debug_img)
                
            # display real-time FPS counter (if valid)
            if rt_fps_valid == True and bShowFPS:
                cv2.putText(output,rt_fps_message, (rt_fps_x,rt_fps_y),text_fontType,text_fontSize,text_color,text_lineSize,text_lineType)

            if bViewOutput:                
                # show the output image
                cv2.imshow(app_main_title, output)
            
            # TODO: enable this through web app?
            frames += [output]
                
        cv2.waitKey(1)

        # Update the real-time FPS counter
        rt_fps_count = rt_fps_count + 1
        if rt_fps_count == 10:
            t = (cv2.getTickCount() - rt_fps_time)/cv2.getTickFrequency()
            rt_fps_valid = 1
            rt_fps = 10.0/t
            rt_fps_message = "FPS: {0:.2f}".format(rt_fps)
            #print("[INFO] ",rt_fps_message)
            rt_fps_count = 0


except KeyboardInterrupt:
    print("Process interrupted by user.")

finally:
    # Get the size of the first frame (ensure all frames are the same size)
    height, width, _ = frames[0].shape

    # Create a unique filename using the current time or any other method you prefer
    unique_filename = f"{int(time.time())}.mp4"  # Unique name based on timestamp

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for MP4 format (or another codec)
    # TODO: this fps might not reflect the fluctuating framerate of processing while playing
    fps = 20  # Frames per second, adjust based on your needs
    output_video = cv2.VideoWriter(unique_filename, fourcc, fps, (width, height))

    # Write frames to video
    for frame in frames:
        output_video.write(frame)  # Write each frame to the video

    # Cleanup
    output_video.release()
    f_profile_csv.close()
    cv2.destroyAllWindows()
