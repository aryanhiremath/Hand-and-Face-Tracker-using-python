import cv2
import mediapipe as mp

# Initialize Mediapipe Face Detection and Drawing utilities
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit()

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

        # Process the frame for face detection
        results = face_detection.process(rgb_frame)

        # Draw face detection annotations
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(frame, detection)

        # Display the frame
        cv2.imshow("Face Tracking", frame)

        # Exit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
