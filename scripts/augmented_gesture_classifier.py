
import numpy as np

class GestureClassifier:
    def classify(self, landmarks):
        if not landmarks:
            return "No Hand"
        
        # Landmarks for finger tips and base joints
        thumb_tip = landmarks[4]
        thumb_base = landmarks[2]
        index_tip = landmarks[8]
        index_base = landmarks[5]
        middle_tip = landmarks[12]
        middle_base = landmarks[9]
        ring_tip = landmarks[16]
        ring_base = landmarks[13]
        pinky_tip = landmarks[20]
        pinky_base = landmarks[17]
        
        # Helper function to determine if a finger is lifted
        def is_finger_lifted(tip, base):
            return tip[1] < base[1]  # Assuming Y-coordinate increases downwards

        # Classify each finger
        fingers_lifted = []
        if is_finger_lifted(thumb_tip, thumb_base):
            fingers_lifted.append("Thumb")
        if is_finger_lifted(index_tip, index_base):
            fingers_lifted.append("Index")
        if is_finger_lifted(middle_tip, middle_base):
            fingers_lifted.append("Middle")
        if is_finger_lifted(ring_tip, ring_base):
            fingers_lifted.append("Ring")
        if is_finger_lifted(pinky_tip, pinky_base):
            fingers_lifted.append("Pinky")

        # Return classifications based on lifted fingers
        if not fingers_lifted:
            return "No Fingers Lifted"
        else:
            return "{} Lifted".format(", ".join(fingers_lifted))
