import os
import cv2
import face_recognition
import pickle

# Directory containing images of known individuals
KNOWN_FACES_DIR = "/home/pi/FaceAuth/Faces"
# File to store known face encodings and names
ENCODINGS_FILE = "/home/pi/FaceAuth/encodings.pickle"

# Initialize lists for known face encodings and names
known_face_encodings = []
known_face_names = []

# Iterate over each person in the training directory
for person_name in os.listdir(KNOWN_FACES_DIR):
    person_dir = os.path.join(KNOWN_FACES_DIR, person_name)
    
    # Only proceed if the path is a directory
    if os.path.isdir(person_dir):
        # Iterate over each image file in the person's directory
        for filename in os.listdir(person_dir):
            filepath = os.path.join(person_dir, filename)
            # Load the image file
            image = cv2.imread(filepath)
            # Convert the image from BGR to RGB (required by face_recognition)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Detect face locations and face encodings
            face_encodings = face_recognition.face_encodings(rgb_image)
            # Assuming each image has exactly one face, add the encoding and name
            if face_encodings:
                # Only take the first face encoding (if multiple faces are detected)
                face_encoding = face_encodings[0]
                known_face_encodings.append(face_encoding)
                known_face_names.append(person_name)

# Save the encodings and names to a pickle file
data = {"encodings": known_face_encodings, "names": known_face_names}
with open(ENCODINGS_FILE, 'wb') as f:
    pickle.dump(data, f)

print(f"Encodings and names have been saved to {ENCODINGS_FILE}")
