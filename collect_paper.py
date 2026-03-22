import socket
import numpy as np
import cv2
import os

os.makedirs('data_esp/paper', exist_ok=True)
ESP32_IP = '172.20.10.11'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ESP32_IP, PORT))
print("Connected! Show PAPER - SPACE=save, Q=quit")

count = 0
while True:
    size_data = client.recv(4)
    size = int.from_bytes(size_data, 'big')
    data = b''
    while len(data) < size:
        packet = client.recv(size - len(data))
        if not packet:
            break
        data += packet
    
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    
    if img is not None:
        img_big = cv2.resize(img, (320,320))
        cv2.putText(img_big, f'paper: {count}/100', (10,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.imshow('Collect Paper', img_big)
    
    key = cv2.waitKey(1)
    if key == 32:
        cv2.imwrite(f'data_esp/paper/paper_{count}.bmp', img)
        count += 1
        print(f'Saved {count}/100')
    elif key == ord('q'):
        break

client.close()
cv2.destroyAllWindows()
print("Done!")
