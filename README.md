# SecureFaceLink

## Overview

The Secure Face Authentication System is a project that implements a robust and secure client-server architecture for face authentication using a Raspberry Pi. The system leverages advanced cryptographic techniques, including AES encryption and TLS, to ensure the confidentiality, integrity, and authenticity of communications between the Raspberry Pi (client) and a remote server (PC). Additionally, the project employs OpenCV and the `face_recognition` library to accurately identify and authenticate users in real-time.

## Features

- **Secure Communication**: Utilizes AES encryption for message security and TLS for secure communication between client and server.
- **Face Detection and Recognition**: Implements real-time face detection and recognition using Haar cascades and the `face_recognition` library.
- **Automated Operation**: The system is designed to run continuously with minimal manual intervention, ensuring real-time authentication and logging of requests and responses.
- **Cross-Platform Compatibility**: The project can be run on various platforms, with the Raspberry Pi serving as the core hardware for image capture and processing.

## Prerequisites

Before running this project, ensure that you have the following installed:

- Python 3.7 or later
- OpenCV
- `face_recognition` library
- `cryptography` library
- A Raspberry Pi with a connected USB camera
- A server (PC) capable of running Python scripts and handling SSL/TLS connections

## Installation
**Clone the Repository**
   git clone https://github.com/gautamsontu/SecureFaceLink.git
Install Required Python Packages


pip install -r requirements.txt
Generate SSL/TLS Certificates

On the Raspberry Pi (client), generate the SSL/TLS certificates:

openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes
Generate AES Key

python generate_key.py  # This script generates a 256-bit key and saves it as 'secret.key'

Transfer the Key
Securely transfer the generated secret.key file from the Raspberry Pi to the server using SCP:


scp /path/to/secret.key pi@<IP_Address>:/home/pi/FaceAuth/
Usage
Running the Server (PC)
Ensure the secret.key is in the correct directory on the server.
Start the server script:

python3 server_script.py
Running the Client (Raspberry Pi)
Ensure the Raspberry Pi has the necessary packages and files.
Start the client script:

python3 main.py
Testing the System
Use the provided web interface to send a "Request Access" command to the Raspberry Pi.
The Raspberry Pi captures an image, processes it, and returns an authentication response to the server.
The server then displays the result on the web interface.
Project Structure

├── FaceAuth/
│   ├── encodings.pickle       # Pre-stored face encodings
│   ├── haarcascade_frontalface_default.xml  # Haarcascade XML for face detection
│   ├── secret.key             # AES key for encryption/decryption
│   ├── server.crt             # SSL/TLS certificate
│   ├── server.key             # SSL/TLS private key
│   ├── main.py                # Client script for Raspberry Pi
│   └── Requests/              # Directory to store images of recognized faces
├── server_script.py           # Server script for handling requests
├── generate_key.py            # Script to generate a 256-bit AES key
├── index.html                 # Web interface for sending authentication requests
└── README.md                  # Project documentation
Security Considerations
Ensure that the secret.key file is securely stored and transferred between devices to prevent unauthorized access.
The SSL/TLS certificates should be generated with a strong key length (e.g., 4096 bits) to ensure secure communication.
Regularly update the dependencies and perform security audits to ensure the system remains secure against potential vulnerabilities.

Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

Acknowledgements
This project uses the cryptography library for encryption, OpenCV for image processing, and face_recognition for facial recognition.
Special thanks to the contributors and open-source community for their valuable libraries and tools.


### Explanation:

- **Overview**: Provides a summary of the project, emphasizing its key features.
- **Prerequisites**: Lists the necessary software and hardware to run the project.
- **Installation**: Guides the user through cloning the repository, installing dependencies, generating keys and certificates, and transferring the key securely.
- **Usage**: Instructions for running the server and client scripts, and testing the system.
- **Project Structure**: A high-level overview of the directory structure and key files.
- **Security Considerations**: Highlights the importance of secure key management and regular updates.
- **License and Contributions**: Details about licensing and how to contribute to the project.
