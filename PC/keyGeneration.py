from cryptography.hazmat.primitives.ciphers import algorithms
import os


key_size = 256
key = os.urandom(key_size // 8)  


with open('secret.key', 'wb') as key_file:
    key_file.write(key)

print("256-bit key generated and saved to secret.key")
