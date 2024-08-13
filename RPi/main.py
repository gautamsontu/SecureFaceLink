
from cryptography.fernet import Fernet
import socket
import ssl
import cv2
import face_recognition
import pickle
import time
import os


with open('secret.key', 'rb') as key_file:
    key = key_file.read()


def encrypt_message(message):
    iv = os.urandom(16)  # AES requires a 16-byte IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = iv + encryptor.update(message.encode()) + encryptor.finalize()
    return encrypted_message

def decrypt_message(encrypted_message):
    iv = encrypted_message[:16]  
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message[16:]) + decryptor.finalize()
    return decrypted_message.decode()


CASCADE_PATH = '/home/pi/FaceAuth/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)


ENCODINGS_PATH = '/home/pi/FaceAuth/encodings.pickle'
with open(ENCODINGS_PATH, 'rb') as file:
    data = pickle.load(file)
    if isinstance(data, dict):
        known_face_encodings = data.get('encodings', [])
        known_face_names = data.get('names', [])
    else:
        raise ValueError("Encodings data should be a dictionary with 'encodings' and 'names' keys.")


REQUESTS_DIR = '/home/pi/FaceAuth/Requests'
os.makedirs(REQUESTS_DIR, exist_ok=True)


ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = ssl_context.wrap_socket(server_socket, server_side=True)

server_socket.bind(('0.0.0.0', 1234))
server_socket.listen(1)
print("Secure server is listening for connections...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Secure connection from {client_address} has been established.")

    try:
       
        encrypted_message = client_socket.recv(1024)
        message = cipher_suite.decrypt(encrypted_message).decode()


   
        if message == "Request Access":
    
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Could not open the camera.")
                response = "Error, Not Authenticated"
            else:
                time.sleep(2) 

                
                ret, frame = cap.read()
                cap.release()

                if not ret:
                    print("Error: Could not read frame.")
                    response = "Error, Not Authenticated"
                else:
                   
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                   
                    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                    if len(faces) == 0:
                        response = "Unknown, Not Authenticated"
                    else:
                        for (x, y, w, h) in faces:
                            
                            roi_color = frame[y:y+h, x:x+w]

                            
                            rgb_roi = cv2.cvtColor(roi_color, cv2.COLOR_BGR2RGB)

                            
                            face_encodings = face_recognition.face_encodings(rgb_roi)

                            if face_encodings:
                                face_encoding = face_encodings[0]

                                
                                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                                name = "Unknown"

                                
                                if True in matches:
                                    first_match_index = matches.index(True)
                                    name = known_face_names[first_match_index]
                                    response = f"{name}, Authenticated"

                                   
                                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                                    
                                    cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                                   
                                    image_path = os.path.join(REQUESTS_DIR, f"{name}_{time.strftime('%Y%m%d_%H%M%S')}.png")
                                    cv2.imwrite(image_path, frame)
                                    print(f"Image saved: {image_path}")
                                    break
                            else:
                                response = "Unknown, Not Authenticated"
        else:
            response = "Invalid Request, Not Authenticated"

    
        encrypted_response = cipher_suite.encrypt(response.encode())
        client_socket.sendall(encrypted_response)

    except Exception as e:
        print(f"An error occurred: {e}")
        client_socket.close()
        continue

    client_socket.close()
