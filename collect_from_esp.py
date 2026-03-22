import socket
import numpy as np
import cv2
import os

classes = ['rock', 'paper', 'scissors']
ESP32_IP = '172.20.10.11'
PORT = 5000

for gesture in classes:
    os.makedirs(f'data_esp/{gesture}', exist_ok=True)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ESP32_IP, PORT))
print("Connected! SPACE=save, Q=next gesture")

current = 0
count = 0
gesture = classes[current]
print(f"Show {gesture.upper()}")

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
        cv2.putText(img_big, f'{gesture}: {count}/100', (10,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.imshow('Collect ESP', img_big)
    
    key = cv2.waitKey(1)
    if key == 32:
        path = f'data_esp/{gesture}/{gesture}_{count}.bmp'
        cv2.imwrite(path, img)
        count += 1
        print(f'Saved {count}/100')
    elif key == ord('q'):
        current += 1
        count = 0
        if current >= len(classes):
            break
        gesture = classes[current]
        print(f"Now show {gesture.upper()}")

client.close()
cv2.destroyAllWindows()
print("Done collecting!")
