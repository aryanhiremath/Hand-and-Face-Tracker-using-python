import cv2
import mediapipe as mp

# Initialize Mediapipe Hands and Face Detection utilities
mp_hands = mp.solutions.hands
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit()

# Setup Mediapipe Hand Tracking
with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

    # Setup Mediapipe Face Detection
    with mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5) as face_detection:

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read frame.")
                break

            # Flip the frame for a mirrored view
            frame = cv2.flip(frame, 1)

            # Convert to RGB for Mediapipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame for hand landmarks
            hand_results = hands.process(rgb_frame)

            # Process the frame for face detection
            face_results = face_detection.process(rgb_frame)

            # Draw landmarks and connections for hands
            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
                    )

            # Draw face detection annotations
            if face_results.detections:
                for detection in face_results.detections:
                    mp_drawing.draw_detection(frame, detection)

            # Display the frame with both hand and face annotations
            cv2.imshow("Hand and Face Tracking", frame)

            # Exit with 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Release resources
cap.release()
cv2.destroyAllWindows()
