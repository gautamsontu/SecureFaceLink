import cv2
import face_recognition
import numpy as np
import pickle

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load known face encodings and names
with open('encodings.pickle', 'rb') as file:
    data = pickle.load(file)
    if isinstance(data, dict):
        known_face_encodings = data.get('encodings', [])
        known_face_names = data.get('names', [])
    else:
        raise ValueError("Encodings data should be a dictionary with 'encodings' and 'names' keys.")

# Initialize the video capture
cap = cv2.VideoCapture(0)  # Use the appropriate camera index

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

print("Starting the camera. Press 'q' to quit.")

while True:
    # Capture a single frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces using Haar Cascade
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Initialize an array to hold the names of detected people
    detected_names = []

    for (x, y, w, h) in faces:
        # Extract the region of interest (ROI) for the detected face
        roi_color = frame[y:y+h, x:x+w]

        # Convert the ROI to RGB format for face recognition
        rgb_roi = cv2.cvtColor(roi_color, cv2.COLOR_BGR2RGB)

        # Encode the face ROI
        face_encoding = face_recognition.face_encodings(rgb_roi)
        if face_encoding:
            face_encoding = face_encoding[0]

            # Compare the face encoding with known face encodings
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match is found, use the first one
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Add the name to the list of detected people
            detected_names.append(name)

            # Draw a rectangle around the detected face and label it
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the display window
cap.release()
cv2.destroyAllWindows()
