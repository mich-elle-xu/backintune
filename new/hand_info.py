import numpy as np
from collections import deque

class Hand: 
    def __init__(self, len_data, handedness): 
        self.handedness = handedness
        self.hand_angles = np.zeros(len_data) 
        self.neutral = np.array([0, 1])
        self.all_angles = []
    
    def angle_between_vectors_np(self, v):
        angle_radians = np.arctan2(
            v[1] * self.neutral[0] - v[0] * self.neutral[1],
            np.dot(self.neutral, v)
        )
        # cos_theta = np.dot(self.neutral, v) / (np.linalg.norm(self.neutral) * np.linalg.norm(v))
        # angle_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))
        # angle_deg = np.degrees(angle_rad)
        angle_deg = np.degrees(angle_radians)
        return float(angle_deg)

    def add_angle(self, angle): 
        # self.hand_angles = self.hand_angles[1:]
        print("deleting from hand_angles")
        # np.delete(self.hand_angles, 0)
        self.hand_angles = np.roll(self.hand_angles,-1)
        self.hand_angles[-1] = angle
        print("adding ", angle, "to hand_hangles")
        # np.append(self.hand_angles, angle)
        print(self.hand_angles)
        self.all_angles.append(angle)
    

    