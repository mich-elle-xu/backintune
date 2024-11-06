# import everything 

import cv2
import mediapipe as mp
from matplotlib import pyplot as plt
import numpy as np
import time
from hand_info import Hand

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
# mp_pose = mp.solutions.pose

def main(): 
    right_hand = Hand(10, "right")
    left_hand = Hand(10, "left")
    # create 2 hand objects, one left one right
    cap = cv2.VideoCapture(0)
    start = time.time()
    with mp_hands.Hands(model_complexity=0,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5) as hands: 
        while cap.isOpened(): 
            success, image = cap.read()
            if not success: 
                print("Ignoring empty camera frame.")
                # use break if using video NOT live 
                continue 
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = hands.process(image)

            if results.multi_hand_landmarks: 
                for ind, landmark in enumerate(results.multi_hand_landmarks): 
                    # print(type(landmark))
                    # mp_drawing.draw_landmarks(
                    #     image,
                    #     landmark,
                    #     mp_hands.HAND_CONNECTIONS,
                    #     mp_drawing_styles.get_default_hand_landmarks_style(),
                    #     mp_drawing_styles.get_default_hand_connections_style())
                    print(ind)
                    label = results.multi_handedness[ind].classification[0].label
                    if label == "Right":
                        wrist_pos = np.array([landmark.landmark[0].x, landmark.landmark[0].y])
                        middle_pos = np.array([landmark.landmark[9].x, landmark.landmark[9].y])
                        cur_vector = np.subtract(middle_pos, wrist_pos)
                        right_hand.add_angle(right_hand.angle_between_vectors_np(cur_vector))
                        print("wrist pos is: ", wrist_pos)
                        print("middle pos is: ", middle_pos)
                        print("cur vector is: ", cur_vector)
                        print(right_hand.hand_angles)
                        # print(right_hand.all_angles)

                    if label == "Left":
                        wrist_pos = np.array([landmark.landmark[0].x, landmark.landmark[0].y])
                        middle_pos = np.array([landmark.landmark[9].x, landmark.landmark[9].y])
                        cur_vector = np.subtract(middle_pos, wrist_pos)
                        left_hand.add_angle(left_hand.angle_between_vectors_np(cur_vector))
                        print("wrist pos is: ", wrist_pos)
                        print("middle pos is: ", middle_pos)
                        print("cur vector is: ", cur_vector)
                        print(left_hand.hand_angles)
                        # print(left_hand.all_angles)
                '''
                    if neutral exists: 
                        for each hand: 
                        record point 0 & 9 
                        get vetor between 0 & 9 
                        calculate angle betwene 0 & 9 vector & neutral 
                        update to hand object data 
                '''
                ''' track 3 things: 
                    deviation from neutral w/ angles 
                    span of hand 
                '''
                # pass
            else: 
                print("No hands detected, ignoring frame.")
            # if there's been an update to the data 
                # check for tension 
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == ord("q"):
                print(left_hand.all_angles)
                print(right_hand.all_angles)
                break
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