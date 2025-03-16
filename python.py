# This script demonstrates basic cryptography using AES encryption in CBC mode on a Raspberry Pi Pico.
# It runs on MicroPython, takes user input via a terminal, encrypts a message, and formats the output.
# The script ensures that sensitive data (key and IV) is stored only in RAM and erased on power-off.

# Import modules for AES encryption and binary/hex conversions
from ucryptolib import aes
import ubinascii  # MicroPython module for converting between binary and hex

# Display welcome message in the terminal
print("Pico Message Gadget")

# Prompt user to enter the message (any characters, including spaces)
message = input("Enter characters including spaces: ")

# Prompt user for a 32-character hexadecimal secret key (16 bytes for AES-128)
# Note: We assume correct input as per instructions (no validation needed)
key_hex = input("Enter 32 capital hex letters, this is a one time secret key: ")

# Prompt user for a 32-character hexadecimal IV (16 bytes for AES-CBC)
# Note: The query says "16 capital hex letters" (8 bytes), but AES-CBC requires 16 bytes (32 hex chars).
# We assume this is a typo and adjust to 32 characters for correctness.
iv_hex = input("Enter Initialisation Vector 32 capital hex letters this is PKCS5 padding: ")

# Convert the hexadecimal key and IV to bytes
# ubinascii.unhexlify converts a hex string (e.g., "1A2B3C") to bytes (b'\x1a\x2b\x3c')
key = ubinascii.unhexlify(key_hex)
iv = ubinascii.unhexlify(iv_hex)

# Convert the message string to bytes using UTF-8 encoding
message_bytes = message.encode('utf-8')

# Apply PKCS5/PKCS7 padding to make the message length a multiple of the AES block size (16 bytes)
# Padding adds N bytes of value N, where N is the number of bytes needed to reach the next multiple
block_size = 16
pad_len = block_size - (len(message_bytes) % block_size)
if pad_len == 0:
    pad_len = block_size  # If length is already a multiple, add a full block
padding = bytes([pad_len]) * pad_len  # Create padding (e.g., 6 bytes of value 6)
padded_message = message_bytes + padding

# Create an AES cipher object in CBC mode (mode=2) with the key and IV
cipher = aes(key, 2, iv)

# Encrypt the padded message using AES-CBC
ciphertext = cipher.encrypt(padded_message)

# Convert the encrypted bytes to an uppercase hexadecimal string
# ubinascii.hexlify converts bytes to hex (e.g., b'\x1a\x2b' to b'1a2b'), then decode to string
hex_str = ubinascii.hexlify(ciphertext).decode('ascii').upper()

# Format and display the hex string in the terminal
# Output format: 5 groups of 5 characters per line, 10 lines per block, 3 blank lines between blocks
line_num = 1
while hex_str:
    # Start each line with a two-digit line number
    line = str(line_num).rjust(2) + ' '
    # Add up to 5 groups of 5 characters
    for _ in range(5):
        if hex_str:
            group = hex_str[:5]  # Take next 5 characters
            hex_str = hex_str[5:]  # Remove them from the string
            line += group + ' '  # Add group with a space
        else:
            break  # Stop if no more characters
    print(line.rstrip())  # Print the line, removing trailing spaces
    # After every 10 lines, add 3 blank lines to separate blocks
    if line_num % 10 == 0:
        print()  # First blank line
        print()  # Second blank line
        print()  # Third blank line
    line_num += 1

# Inform the user that keys will be erased when the terminal closes
print("The keys will now be erased from temporary RAM in the R Pi when window closes")

# No explicit clearing of variables is needed; Pico's RAM is volatile and clears on power-off #
# When the user closes the terminal and disconnects the Pico, all data in RAM is lost #
