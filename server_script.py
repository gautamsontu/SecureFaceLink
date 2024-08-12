from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import socket
import ssl
import os

# Load the 512-bit key from the 'secret.key' file
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

# Function to encrypt a message using AES with a 512-bit key
def encrypt_message(message):
    iv = os.urandom(16)  # Generate a random 16-byte IV (Initialization Vector)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = iv + encryptor.update(message.encode()) + encryptor.finalize()
    return encrypted_message

# Function to decrypt a message using AES with a 512-bit key
def decrypt_message(encrypted_message):
    iv = encrypted_message[:16]  # Extract the IV from the beginning of the encrypted message
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message[16:]) + decryptor.finalize()
    return decrypted_message.decode()

RPi_IP_Address = '10.0.0.36'

# Secure message
message = "Request Access"
encrypted_message = encrypt_message(message)

# Create a context for secure communication
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Connect to the server securely
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_socket = ssl_context.wrap_socket(client_socket, server_hostname=RPi_IP_Address)

secure_socket.connect((RPi_IP_Address, 12345))
secure_socket.sendall(encrypted_message)

# Receive and decrypt the response
response = secure_socket.recv(1024)
decrypted_response = decrypt_message(response)
print("Server Response:", decrypted_response)

# Close the socket
secure_socket.close()
