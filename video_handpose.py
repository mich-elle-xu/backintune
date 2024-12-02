# import everything 

import cv2
import mediapipe as mp
from matplotlib import pyplot as plt
import numpy as np
import time
from hand_info import Hand
import os

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
output_dir = "angle_outputs/above_new"
input_dir = "recordings/above"

def main(): 
    for root, _, files in os.walk(input_dir):
        print(input_dir)
        for file_name in files:
            input_path = os.path.join(root, file_name)
            
            # Remove the .mov extension for the output file name
            output_file_name = os.path.splitext(file_name)[0]
            output_path = os.path.join(output_dir, output_file_name)
            data = tense_routine(input_path)
            with open(output_path, "w") as f:
                    for hand in data:
                        f.write(str(hand))
                        f.write("\n")
                    print(f"Processed {input_path} and saved output to {output_path}")


def tense_routine(video_path): 
    right_hand = Hand(10, "right")
    left_hand = Hand(10, "left")
    # create 2 hand objects, one left one right
    cap = cv2.VideoCapture(video_path)
    # print(cap.get(cv2.CAP_PROP_FPS))
    fps = int(cap.get(5))
    start = time.time()
    with mp_hands.Hands(model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.3) as hands: 
        while cap.isOpened(): 
            success, image = cap.read()
            if not success: 
                print("Ignoring empty camera frame.")
                # use break if using video NOT live 
                break 
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = hands.process(image)

            if results.multi_hand_landmarks: 
                for ind, landmark in enumerate(results.multi_hand_landmarks): 
                    mp_drawing.draw_landmarks(
                        image,
                        landmark,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                    # print(ind)
                for ind in range(len(results.multi_handedness)):
                    label = results.multi_handedness[ind].classification[0].label
                    if label == "Right":
                        wrist_pos = np.array([landmark.landmark[0].x, landmark.landmark[0].y])
                        middle_pos = np.array([landmark.landmark[9].x, landmark.landmark[9].y])
                        cur_vector = np.subtract(middle_pos, wrist_pos)
                        thumb_pos = np.array([landmark.landmark[2].x, landmark.landmark[2].y])
                        pinky_pos = np.array([landmark.landmark[17].x, landmark.landmark[17].y]) 
                        span = np.linalg.norm(thumb_pos - pinky_pos)
                        right_hand.add_span(span)
                        right_hand.add_angle(right_hand.angle_between_vectors_np(cur_vector))
                        # print("wrist pos is: ", wrist_pos)
                        # print("middle pos is: ", middle_pos)
                        # print("cur vector is: ", cur_vector)
                        # print(right_hand.hand_angles)
                        # print(right_hand.all_angles)

                    if label == "Left":
                        wrist_pos = np.array([landmark.landmark[0].x, landmark.landmark[0].y])
                        middle_pos = np.array([landmark.landmark[9].x, landmark.landmark[9].y])
                        cur_vector = np.subtract(middle_pos, wrist_pos)
                        thumb_pos = np.array([landmark.landmark[2].x, landmark.landmark[2].y])
                        pinky_pos = np.array([landmark.landmark[17].x, landmark.landmark[17].y]) 
                        span = np.linalg.norm(thumb_pos - pinky_pos)
                        left_hand.add_span(span)
                        left_hand.add_angle(left_hand.angle_between_vectors_np(cur_vector))
                        # print("wrist pos is: ", wrist_pos)
                        # print("middle pos is: ", middle_pos)
                        # print("cur vector is: ", cur_vector)
                        # print(left_hand.hand_angles)
                        # print(left_hand.all_angles)
            else: 
                print("No hands detected, ignoring frame.")
            # if there's been an update to the data 
                # check for tension 
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == ord("q"):
                print("RETURNING FROM TENSE ROUTINE")
                break
                # return(right_hand.all_angles, left_hand.all_angles)
                print(left_hand.all_angles)
                print(right_hand.all_angles)
                break
        return(right_hand.all_angles, right_hand.spans, left_hand.all_angles, left_hand.spans)
        cap.release()
if __name__ == "__main__":
    main()



'''
main: 
    open video 
    with hands as hands 
        while cap.isOpened
            read output 
            if not success, continue/ break
            if hands detected: 
                draw landmarks if in debug mode 
                if neutral has been recorded: 
                    get curent vector
                    calculate angle betwen cur & neutral 
                    add to data 
            else: 
                continue 
    
        check for tension

def main():            
'''