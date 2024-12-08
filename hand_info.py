import numpy as np
from collections import deque
import random 

class Hand: 
    def __init__(self, len_data, handedness): 
        self.handedness = handedness
        self.hand_angles = np.zeros(len_data) 
        self.tension_states = np.zeros(len_data)
        self.all_tensions = []
        self.tense = False
        self.neutral = np.array([0, 1])
        self.all_angles = []
        self.spans = []
    
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
    
    def add_span(self, span): 
        self.spans.append(span)

    def add_angle(self, angle): 
        # self.hand_angles = self.hand_angles[1:]
        # print("deleting from hand_angles")
        # np.delete(self.hand_angles, 0)
        self.hand_angles = np.roll(self.hand_angles,-1)
        self.hand_angles[-1] = angle
        # print("adding ", angle, "to hand_hangles")
        # np.append(self.hand_angles, angle)
        # print(self.hand_angles)
        self.all_angles.append(angle)

    def update_tension_states(self, threshold=0.5, window_size=3):
        # Compute the difference between consecutive wrist angles (rate of change)
        angle_changes = np.abs(np.diff(self.hand_angles, n=1))
        
        # Create a sliding window of changes and compute the average change in that window
        avg_changes = np.convolve(angle_changes, np.ones(window_size), mode='same') / window_size
        
        # Areas where the average change is less than the threshold are considered 'tension'
        tension_zones = avg_changes < threshold
        tension_zones = np.concatenate(([False], tension_zones))
        
        is_tension = np.sum(tension_zones) > (len(tension_zones) / 2)
        print(self.handedness + ": " + str(is_tension))

        self.tension_states = np.roll(self.tension_states,-1)
        self.all_tensions.append(is_tension)
        self.tension_states[-1] = is_tension
        return is_tension

    def update_tension(self): 
        temp = 0
        for val in self.tensions_states: 
            if val: 
                temp += 1
        if temp > len(self.tensions_states) / 2: 
            self.tense = True