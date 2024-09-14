import numpy as np

class GestureClassifier:
    def classify(self, landmarks):
        if not landmarks:
            return "No Hand"
        
        # Example logic: Compare distances between landmarks
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]

        avg_tip_distance = np.mean([
            np.linalg.norm(np.array(thumb_tip) - np.array(index_tip)),
            np.linalg.norm(np.array(thumb_tip) - np.array(middle_tip)),
            np.linalg.norm(np.array(thumb_tip) - np.array(ring_tip)),
            np.linalg.norm(np.array(thumb_tip) - np.array(pinky_tip))
        ])

        # Simple threshold to differentiate between open and closed hand
        if avg_tip_distance > 0.1:
            return "Open Hand"
        else:
            return "Closed Fist"

