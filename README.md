# How It Works: MicroPython Version
The **Pico Message Gadget** is a message encryption tool designed for the Raspberry Pi Pico, running MicroPython. This version uses AES-CBC encryption with PKCS5/PKCS7 padding via the `ucryptolib` module. Below is a detailed explanation of how it works, how to set it up, and how to deploy it as a `.uf2` file.
---
## Setup
- **Hardware Connection**: The Raspberry Pi Pico, with MicroPython installed, connects to your PC via a USB cable. It appears as a virtual COM port (e.g., COM3 on Windows) for serial communication.
- **Script Execution**: When the MicroPython script (`main.py`) runs—automatically on boot—it communicates with your PC over this serial interface using the Pico’s USB stdio.
---
## User Interaction
1. **Terminal Prompt**: 
   - Open a terminal program (e.g., PuTTY or Thonny’s terminal) set to 115200 baud.
   - The terminal displays:  
     ```
     Pico Message Gadget
     ```
2. **Input Process**:
   - **Message**: Enter any text (e.g., "Hello Pico").
   - **Key**: Enter a 32-character hexadecimal string (16 bytes), e.g., `0123456789ABCDEF0123456789ABCDEF`.
   - **IV (Initialization Vector)**: Enter another 32-character hex string (16 bytes), e.g., `FEDCBA9876543210FEDCBA9876543210`.
     These inputs are collected via the terminal and validated for correct length and format.
---
## Encryption
- **Encoding**: The user’s message is converted from a string to bytes (e.g., `"Hello Pico"` becomes `b'Hello Pico'`).
- **Padding**: The message is padded to a multiple of 16 bytes using PKCS5/PKCS7 padding, as required by AES-CBC. For example, a 10-byte message like `"Hello Pico"` gets 6 bytes of padding (each byte is `0x06`).
- **AES-CBC Encryption**: The `ucryptolib` module encrypts the padded message using:
  - **Mode**: AES-CBC (Cipher Block Chaining).
  - **Key**: The 16-byte key provided by the user.
  - **IV**: The 16-byte initialization vector provided by the user.
- **Result**: A ciphertext in bytes is generated.
---
## Output Formatting
- **Hex Conversion**: The ciphertext bytes are converted to an uppercase hexadecimal string (e.g., a 16-byte ciphertext becomes a 32-character hex string like `0123456789ABCDEF0123456789ABCDEF`).
- **Grouping**: The hex string is split into:
  - Groups of 5 characters (e.g., `01234`, `56789`).
  - 5 groups per line (if possible).
  - Each line is numbered on the left (starting from 1).
- **Blocking**: Every 10 lines form a block, separated by 3 blank lines (e.g., lines 1-10, then blank lines, then 11-20).
- **Example Output** (for a 16-byte ciphertext, 32 hex characters):
  ```
  1 01234 56789 ABCDE F0123 45678
  2 9ABCD EF012
  ```
- **User Action**: Copy the output from the terminal (e.g., `Ctrl+Shift+C` in PuTTY) and paste it into a text file for later use.
---
## Security
- **Key and IV Storage**: The key and IV are stored in the Pico’s RAM only during script execution.
- **Clearing RAM**: When you close the terminal and disconnect or power off the Pico, the RAM clears naturally, erasing the key and IV.
---
## Compiling and Deploying to a .uf2 File
To make this project easily deployable in Post Doc Bucket 1, we drag-and-dropt the  `.uf2` file, follow these steps:
### Step 1: Install MicroPython on the Pico
1. **Download Firmware**: Get the latest MicroPython `.uf2` file for the Raspberry Pi Pico from [micropython.org](https://micropython.org).
2. **Enter BOOTSEL Mode**: 
   - Hold the **BOOTSEL** button on the Pico.
   - Connect it to your PC via USB.
   - Release the button. The Pico appears as a mass storage device (`RPI-RP2`).
3. **Install MicroPython**: Drag the `.uf2` file onto the Pico. It will install MicroPython, eject itself, and reboot.
### Step 2: Upload the Script as `main.py`
- **Script**: Save the MicroPython script (below) as `main.py` on your PC.
- **Option 1: Using Thonny (Recommended)**:
  1. Install Thonny from [thonny.org](https://thonny.org).
  2. Connect the Pico via USB (no BOOTSEL needed after MicroPython is installed).
  3. In Thonny, go to **File > Save as**.
  4. Select “Raspberry Pi Pico” as the destination.
  5. Name the file `main.py` and click OK to upload.
- **Option 2: Manual Copy**:
  1. Put the Pico into BOOTSEL mode again (hold BOOTSEL, connect USB, release).
  2. Copy `main.py` to the Pico’s filesystem (it appears as a drive).
  3. Disconnect and reconnect the Pico to reboot.
#### Sample `main.py` Script
```python
import ucryptolib
import sys

print("Pico Message Gadget")
message = input("Enter characters including spaces: ")
key = input("Enter 32 capital hex letters (secret key): ")
iv = input("Enter 32 capital hex letters (IV, PKCS7 padding): ")

# Convert hex key and IV to bytes
key = bytes.fromhex(key)
iv = bytes.fromhex(iv)

# Pad message to multiple of 16 bytes (PKCS7)
msg_bytes = message.encode()
pad_len = 16 - (len(msg_bytes) % 16)
msg_bytes += bytes([pad_len]) * pad_len

# Encrypt with AES-CBC
cipher = ucryptolib.aes(key, 2, iv)  # Mode 2 = CBC
ciphertext = cipher.encrypt(msg_bytes)

# Convert ciphertext to hex and format output
hex_str = ciphertext.hex().upper()
lines = [hex_str[i:i+25] for i in range(0, len(hex_str), 25)]
for i, line in enumerate(lines, 1):
    formatted = " ".join(line[j:j+5] for j in range(0, len(line), 5))
    print(f"{i} {formatted}")

print("Keys will be erased from RAM when the terminal closes.")
```
### Step 3: Run the Script
- After uploading `main.py`, the Pico runs it automatically on boot.
- **Open a Terminal**:
  - Use PuTTY or Thonny’s terminal.
  - Find the Pico’s COM port in Device Manager (e.g., COM3).
  - Connect with settings: 115200 baud, 8 data bits, 1 stop bit, no parity.
- The terminal will display “Pico Message Gadget” and prompt for input.
### Single .uf2 Option (Advanced)
- Embedding the script into a custom `.uf2` file requires building MicroPython firmware with the script “frozen” into it using `mpy-cross` and the MicroPython source code. The method above (standard MicroPython `.uf2` + `main.py`) is simpler but if you don't have Thonny parsing libraries correctly then you'll need to build the executable first manually.
---
- **Terminal Use**: 
  - Copy text with `Ctrl+Shift+C` and paste with `Ctrl+Shift+V` in terminals like PuTTY.
- **Implemenation Safety Idea**: Disconnect the Pico after use to ensure RAM clears the key and IV.
- **Learning**: Experiment with different messages to observe ciphertext changes. Keep the key and IV at 32 hex characters (16 bytes) each for AES-CBC compatibility.
---
This MicroPython version provides a simple, accessible way to explore encryption on the Pico, contrasting with the C++ and ARM assembly versions in buckets 2, 3 and so on.
For references on the output format see: https://www.cryptomuseum.com/crypto/otp/index.htm for key exchange: none. Its OTP. Or use a Beale Cipher https://en.wikipedia.org/wiki/Beale_ciphers <80)

⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⢋⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⢾⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⠟⣿⢸⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠠⠤⢤⣤⣤⣴⣤⣤⣤⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣄⣿⣿⣾⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢹⣿⠀⠀⠀⠀⠀⣀⣠⣴⣶⡿⠿⠟⠒⠛⠉⠉⠉⠉⠉⠉⠉⠙⠛⠛⠻⠿⢿⣶⣤⣄⣀⠀⠀⠘⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⠀⢀⣤⣶⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⠿⣶⣤⣿⣿⣿⣿⣟⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣧⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣴⣶⣾⡿⠿⠿⠿⢿⣿⣷⣶⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⢿⣿⡿⠿⠛⣿⡿⠀⠀⢀⣠⣴⣾⣿⡟⠋⠉⠀⠀⠈⢧⡀⣷⣄⡂⠙⢧⡁⡝⢿⣿⣿⣿⣷⣦⣤⣀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣧⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣦⡀⠀⢀⡴⢻⣿⣴⣾⡿⣟⣉⣼⣟⠤⠤⠖⠒⠒⠒⠒⠻⢏⡛⢬⡙⠛⠳⢄⠀⠳⣍⡻⣿⣿⣿⠿⣿⣷⣶⣤⣄⣸⣿⣿⣿⣿⡏⢧⠀⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⢸⢹⠉⠀⢷⡏⢰⡟⠢⡄⢰⣶⣶⣿⣿⣿⣶⡖⠉⠢⢝⡂⠀⠀⠙⠢⢄⣙⣺⣿⣿⣷⣶⢾⡟⢻⣿⣿⣿⣿⣿⣿⠁⢈⡷⣄⢀⣀⣨⠭⠟⣩⣿⣿⣿
⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⡜⣼⠀⢀⠀⣇⣿⣿⣿⡿⠟⣿⣿⣿⡿⣿⢿⣎⣳⢤⣀⠈⠙⢶⡶⠤⢤⣴⣶⣶⣷⣍⣫⡾⣡⣿⠿⣜⡇⠠⢀⡏⠀⢀⢳⡈⠑⢦⣤⣴⣾⣿⣿⣿⣿
⣿⣿⣿⣦⣄⣀⣀⣀⣠⠊⡇⡏⢠⠈⠲⢿⣿⣿⣧⡀⠀⢴⣯⣙⠷⠿⠔⠊⠁⠀⠀⠉⠙⡒⠛⠦⠤⢌⣙⠋⠛⠉⠙⠛⠛⠋⠛⣼⡇⢀⣾⡇⠀⣾⡦⠽⣶⡤⣬⣭⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡿⠿⠟⣡⡞⠁⡟⡆⢳⡀⢆⢿⠻⡑⠞⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⡐⠀⢸⠲⣄⠀⠀⠀⠉⠓⠢⠤⣀⠀⣠⠞⣁⣴⣯⢏⡇⣰⣿⡇⠘⢾⡻⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⢦⢱⢹⡀⠹⣌⢾⢧⠙⠦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⢸⠀⠈⡆⠀⠀⠀⠀⠀⠑⠤⣉⣙⣉⢅⡾⢃⣾⣴⢯⡇⢻⡀⢠⣙⣦⣬⣽⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣷⣶⣶⡇⢸⡘⡄⢻⣄⠙⢿⣶⢵⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢦⢘⣆⣠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠰⢚⣹⢷⣿⡟⢡⣿⠁⠘⣧⡈⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣎⡇⠘⡄⠻⣷⣄⠙⠧⣄⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣼⣋⣴⡿⡼⢀⡀⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⠃⠀⢨⢦⢌⣢⣙⣷⡺⣍⡉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣯⡟⢹⣿⣧⠇⢸⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢠⠀⢳⣷⣌⡙⠻⢧⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠤⣔⣒⠦⠤⠄⠀⠀⠀⠀⠀⠀⢠⢯⣾⢈⢼⡟⠏⢠⢿⢇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⣦⠀⠻⡝⣿⠛⡖⣿⡉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣰⡞⠁⣰⢋⡞⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡼⣿⣷⣄⠹⣼⢯⣷⠘⣿⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠟⣿⣿⣿⣫⣴⢛⢳⣯⣞⣉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠙⣾⣮⣿⣤⣿⣞⣿⣷⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁⢀⣿⣿⣿⣿⣾⣷⣿⡈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢠⣿⣿⣿⣿⣷⣿⣿⣿⣆⠈⠑⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠛⠁⣠⠔⠋⣿⣿⣿⣿⣿⣿⣿⣿⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠃⠐⢋⣾⣿⣿⣿⣾⣿⣿⣿⣿⡀⠀⠀⠀⠉⠒⠤⢄⣀⣀⡠⠔⠋⣀⣠⣤⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⡿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠉⣉⣍⣩⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣎⠉⢃⠈⣼⣿⣿⣿⣿⣿⣿⡿⠟⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣄⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠹⣿⣿⣿⣿⣦⣼⢤⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⣀⣉⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⡀⠀⡏⠹⡟⣿⣿⢀⡎⣽⠋⢰⠁⠀⠀⠀⠀⢀⣠⡴⠿⣛⣭⡷⠿⠛⠋⠉⠁⠀⢀⡤⣺⣷⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠘⡟⣿⣆⡇⠀⢳⣷⣿⣿⢰⠏⠀⢺⣀⠤⠴⣒⣫⣽⣶⠾⠛⠉⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⡏⠀⠀⠙⢮⣙⣷⠄⢀⣿⣿⣧⠋⠤⢒⡏⡔⢛⡉⠁⢀⠉⢀⠀⠀⠀⠀⠀⠀⠀⢀⡠⣻⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⠔⢉
