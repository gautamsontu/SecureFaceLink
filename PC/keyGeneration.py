from cryptography.hazmat.primitives.ciphers import algorithms
import os

# Generate a 256-bit key
key_size = 256
key = os.urandom(key_size // 8)  # Generate a random key of the specified size in bytes

# Save the key to a file (make sure to keep this file secure)
with open('secret.key', 'wb') as key_file:
    key_file.write(key)

print("256-bit key generated and saved to secret.key")
