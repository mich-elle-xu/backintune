import cv2
import mediapipe as mp
from matplotlib import pyplot as plt
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose

def record_neutral(results): 
    wrist_vectors = []
    wrist_joint = 0 
    middle_joint = 9 
    for hand in results.multi_hand_landmarks:
        wrist_pos = np.array([hand.landmark[wrist_joint].x, hand.landmark[wrist_joint].y])
        middle_pos = np.array([hand.landmark[middle_joint].x, hand.landmark[middle_joint].y])
        # print(wrist_pos)
        # print(middle_pos)
        # wrist_vectors.append(np.subtract(middle_pos, wrist_pos))
        wrist_vectors = np.subtract(middle_pos, wrist_pos)
    print(wrist_vectors)

    return(wrist_vectors) 

def angle_between_vectors_np(u, v):
    cos_theta = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    angle_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    angle_deg = np.degrees(angle_rad)
    return angle_rad, angle_deg

def main():
    neutral = None
    # For webcam input:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
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
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                wrist_joint = 0 
                middle_joint = 9 
                if neutral is not None:
                    for hand in results.multi_hand_landmarks:
                        wrist_pos = np.array([hand.landmark[wrist_joint].x, hand.landmark[wrist_joint].y])
                        middle_pos = np.array([hand.landmark[middle_joint].x, hand.landmark[middle_joint].y])
                        vector = np.subtract(middle_pos, wrist_pos)
                        # print(f"neutral = {neutral}")
                        # print(f"vector = {vector}")
                        print(angle_between_vectors_np(vector, neutral))
                    
            
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

            color = (255, 0, 0)
            cv2.putText(image, 'OpenCV', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, color, 2, cv2.LINE_AA) 

            if cv2.waitKey(5) & 0xFF == ord("c"):
                neutral = record_neutral(results)
            if cv2.waitKey(5) & 0xFF == ord("q"):
                break
        cap.release()



if __name__ == "__main__":
    main()
