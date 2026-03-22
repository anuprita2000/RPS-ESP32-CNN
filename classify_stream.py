# ── Rock Paper Scissors - Laptop Classifier Client ──
# Receives camera images streamed from ESP32 over WiFi,
# runs CNN inference on each frame, and displays the
# predicted gesture with confidence in real time.
# Author: Anuprita Kaple, Cornell MEM 5400, 2026

# Import required libraries
import socket        # For WiFi communication with ESP32
import numpy as np   # For array operations
import cv2           # For image display and processing
from tensorflow import keras  # For loading and running CNN model

# Load the trained CNN model (trained on ESP32 camera images)
model = keras.models.load_model('prs_cnn_esp.h5')

# Class labels - must match order used during training
classes = ['rock', 'paper', 'scissors']

# ESP32 IP address (assigned by iPhone hotspot) and port
ESP32_IP = '172.20.10.11'
PORT = 5000

# Connect to ESP32 socket server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ESP32_IP, PORT))
print("Connected to ESP32!")

# Main loop - receive, classify and display each frame
while True:
    # Step 1: Receive 4-byte header to get image size
    size_data = client.recv(4)
    size = int.from_bytes(size_data, 'big')

    # Step 2: Receive full image bytes based on size from header
    data = b''
    while len(data) < size:
        packet = client.recv(size - len(data))
        if not packet:
            break
        data += packet

    # Step 3: Decode received bytes into a grayscale image array
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    if img is not None:
        # Step 4: Resize to 32x32 and normalize for CNN input
        resized = cv2.resize(img, (32, 32))
        input_img = resized.reshape(1, 32, 32, 1) / 255.0

        # Step 5: Run CNN inference - returns probability for each class
        pred = model.predict(input_img, verbose=0)
        label = classes[np.argmax(pred)]       # Class with highest probability
        confidence = np.max(pred) * 100         # Confidence as percentage

        # Step 6: Display image with prediction label and confidence
        img_big = cv2.resize(img, (320, 320))  # Scale up for visibility
        cv2.putText(img_big, f'{label} ({confidence:.0f}%)',
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 255), 2)
        cv2.imshow('RPS Classifier', img_big)

    # Press Q to quit
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up connections and windows
client.close()
cv2.destroyAllWindows()