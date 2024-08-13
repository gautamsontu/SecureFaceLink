
from cryptography.fernet import Fernet
import socket
import ssl
import cv2
import face_recognition
import pickle
import time
import os

# Load the encryption key from the file
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

# Initialize AES cipher for encryption and decryption
def encrypt_message(message):
    iv = os.urandom(16)  # AES requires a 16-byte IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = iv + encryptor.update(message.encode()) + encryptor.finalize()
    return encrypted_message

def decrypt_message(encrypted_message):
    iv = encrypted_message[:16]  # Extract the IV from the beginning
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message[16:]) + decryptor.finalize()
    return decrypted_message.decode()

# Load the Haar Cascade classifier for face detection
CASCADE_PATH = '/home/pi/FaceAuth/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# Load known face encodings and names
ENCODINGS_PATH = '/home/pi/FaceAuth/encodings.pickle'
with open(ENCODINGS_PATH, 'rb') as file:
    data = pickle.load(file)
    if isinstance(data, dict):
        known_face_encodings = data.get('encodings', [])
        known_face_names = data.get('names', [])
    else:
        raise ValueError("Encodings data should be a dictionary with 'encodings' and 'names' keys.")

# Directory to save the detected images
REQUESTS_DIR = '/home/pi/FaceAuth/Requests'
os.makedirs(REQUESTS_DIR, exist_ok=True)

# SSL context setup
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

# Set up server socket with SSL
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = ssl_context.wrap_socket(server_socket, server_side=True)

server_socket.bind(('0.0.0.0', 1234))
server_socket.listen(1)
print("Secure server is listening for connections...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Secure connection from {client_address} has been established.")

    try:
        # Receive and decrypt the message
        encrypted_message = client_socket.recv(1024)
        message = cipher_suite.decrypt(encrypted_message).decode()


        # Check for the specific request message
        if message == "Request Access":
            # Initialize the video capture
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Could not open the camera.")
                response = "Error, Not Authenticated"
            else:
                time.sleep(2)  # Allow the camera to warm up

                # Capture a single frame from the camera
                ret, frame = cap.read()
                cap.release()

                if not ret:
                    print("Error: Could not read frame.")
                    response = "Error, Not Authenticated"
                else:
                    # Convert the frame to grayscale for face detection
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Detect faces using Haar Cascade
                    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                    if len(faces) == 0:
                        response = "Unknown, Not Authenticated"
                    else:
                        for (x, y, w, h) in faces:
                            # Extract the region of interest (ROI) for the detected face
                            roi_color = frame[y:y+h, x:x+w]

                            # Convert the ROI to RGB format for face recognition
                            rgb_roi = cv2.cvtColor(roi_color, cv2.COLOR_BGR2RGB)

                            # Encode the face ROI
                            face_encodings = face_recognition.face_encodings(rgb_roi)

                            if face_encodings:
                                face_encoding = face_encodings[0]

                                # Compare the face encoding with known face encodings
                                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                                name = "Unknown"

                                # If a match is found, use the first one
                                if True in matches:
                                    first_match_index = matches.index(True)
                                    name = known_face_names[first_match_index]
                                    response = f"{name}, Authenticated"

                                    # Draw a rectangle around the face
                                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                                    # Put the name label on the image
                                    cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                                    # Save the detected image with annotation
                                    image_path = os.path.join(REQUESTS_DIR, f"{name}_{time.strftime('%Y%m%d_%H%M%S')}.png")
                                    cv2.imwrite(image_path, frame)
                                    print(f"Image saved: {image_path}")
                                    break
                            else:
                                response = "Unknown, Not Authenticated"
        else:
            response = "Invalid Request, Not Authenticated"

        # Encrypt and send the response
        encrypted_response = cipher_suite.encrypt(response.encode())
        client_socket.sendall(encrypted_response)

    except Exception as e:
        print(f"An error occurred: {e}")
        client_socket.close()
        continue

    client_socket.close()
