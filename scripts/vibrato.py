import cv2
from hand_tracker import HandTracker
from augmented_gesture_classifier import GestureClassifier

def main():
    hand_tracker = HandTracker()
    gesture_classifier = GestureClassifier()

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = hand_tracker.process_frame(frame)
        landmarks = hand_tracker.extract_landmarks(results)
        gesture = gesture_classifier.classify(landmarks)
        print(gesture)

        hand_tracker.draw_landmarks(frame, results)
        cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

