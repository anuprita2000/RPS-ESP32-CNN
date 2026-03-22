import socket
import numpy as np
import cv2

ESP32_IP = '172.20.10.11'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ESP32_IP, PORT))
print("Connected to ESP32!")

while True:
    # Receive image size
    size_data = client.recv(4)
    size = int.from_bytes(size_data, 'big')
    
    # Receive image data
    data = b''
    while len(data) < size:
        packet = client.recv(size - len(data))
        if not packet:
            break
        data += packet
    
    # Decode and display
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    if img is not None:
        img_big = cv2.resize(img, (320, 320))
        cv2.imshow('ESP32 Stream', img_big)
    
    if cv2.waitKey(1) == ord('q'):
        break

client.close()
cv2.destroyAllWindows()
