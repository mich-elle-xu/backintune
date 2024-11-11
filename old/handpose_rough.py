import cv2
import mediapipe as mp
from matplotlib import pyplot as plt
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
hand_refs = dict()
cur_hand_vectors = dict()
hand_angles = dict()
hand_angles["left"] = np.zeros(10)
hand_angles["right"] = np.zeros(10)

def record_neutral(results): 
    wrist_vectors = []
    wrist_joint = 0 
    middle_joint = 9 
    for hand in results.multi_hand_landmarks:
        wrist_pos = np.array([hand.landmark[wrist_joint].x, hand.landmark[wrist_joint].y])
        middle_pos = np.array([hand.landmark[middle_joint].x, hand.landmark[middle_joint].y])
        wrist_vectors.append(np.subtract(middle_pos, wrist_pos))
    print(wrist_vectors)
    return(wrist_vectors) 

def angle_between_vectors_np(u, v):
    cos_theta = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    angle_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    angle_deg = np.degrees(angle_rad)
    return angle_deg

def find_tension(positions):
    print ("standard deviation of positions = " + str(np.std(positions)))

def detect_tension(wrist_angles, left_right, threshold=0.5, window_size=3):
    # Compute the difference between consecutive wrist angles (rate of change)
    angle_changes = np.abs(np.diff(wrist_angles, n=1))
    
    # Create a sliding window of changes and compute the average change in that window
    avg_changes = np.convolve(angle_changes, np.ones(window_size), mode='same') / window_size
    
    # Areas where the average change is less than the threshold are considered 'tension'
    tension_zones = avg_changes < threshold
    tension_zones = np.concatenate(([False], tension_zones))
    
    is_tension = np.sum(tension_zones) > (len(tension_zones) / 2)
    print(left_right + ": " + str(is_tension))
    return is_tension

def main():
    neutral = None
    # For webcam input:
    cap = cv2.VideoCapture(0)
    start = time.time()
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            print('Handedness:', results.multi_handedness)
            if results.multi_hand_landmarks:
                # for hand_landmarks in results.multi_hand_landmarks:
                    # print('hand_landmarks:', hand_landmarks)
                print(results.multi_hand_landmarks)
                # print(results.multi_hand_landmarks["Handedness"])
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                wrist_joint = 0 
                middle_joint = 9 
                wrist_positions = []
                if neutral is not None:
                    # get hand vectors
                    # sort to left right
                    cur_vectors = []
                    for hand in results.multi_hand_landmarks:
                        wrist_pos = np.array([hand.landmark[wrist_joint].x, hand.landmark[wrist_joint].y])
                        middle_pos = np.array([hand.landmark[middle_joint].x, hand.landmark[middle_joint].y])
                        temp = [wrist_pos, middle_pos]
                        wrist_positions.append(temp)
                        # cur_vectors.append(np.subtract(middle_pos, wrist_pos))
                    wrist_positions = sorted(wrist_positions, key=lambda x: x[0][0])
                    # cur_vectors = sorted(cur_vectors, key=lambda x: x[0])
                    for pos in wrist_positions: 
                        cur_vectors.append(np.subtract(middle_pos, wrist_pos))
                    cur_hand_vectors["left"] = cur_vectors[0]
                    cur_hand_vectors["right"] = cur_vectors[1]
                    np.delete(hand_angles["left"], 0)
                    np.delete(hand_angles["right"], 0)
                    cur_left = angle_between_vectors_np(hand_refs["left"], cur_hand_vectors["left"])
                    cur_right = angle_between_vectors_np(hand_refs["right"], cur_hand_vectors["right"])
                    hand_angles["left"] = np.append(hand_angles["left"], cur_left)
                    hand_angles["right"] = np.append(hand_angles["right"], cur_right)
                    np.append(hand_angles["right"], angle_between_vectors_np(hand_refs["right"], cur_hand_vectors["right"]))

                    # print("left status: " + cur_left)
                    # print("right status: " + cur_right)

            detect_tension(hand_angles["left"], "left")
            detect_tension(hand_angles["right"], "right")
            # print(hand_angles["left"])
                # # print(f"neutral = {neutral}")
                # # print(f"vector = {vector}")
                # print(angle_between_vectors_np(vector, neutral))
                    
                    
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

            color = (255, 0, 0)
            cv2.putText(image, 'OpenCV', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, color, 2, cv2.LINE_AA) 

            if cv2.waitKey(5) & 0xFF == ord("c"):
                neutral = record_neutral(results)
                neutral = sorted(neutral, key=lambda x: x[0])
                hand_refs["left"] = neutral[0]
                hand_refs["right"] = neutral[1] 
                print(neutral)
                print(hand_refs)

            if cv2.waitKey(5) & 0xFF == ord("q"):
                break
        cap.release()



if __name__ == "__main__":
    main()
