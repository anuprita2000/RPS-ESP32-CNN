import cv2
import os

gestures = ['rock', 'paper', 'scissors']
print("Press SPACE to capture, Q to move to next gesture.")
cap = cv2.VideoCapture(0)

for gesture in gestures:
    count = 0
    os.makedirs(f'data/{gesture}', exist_ok=True)
    print(f"\nShow {gesture.upper()} close to camera. SPACE=capture, Q=next gesture")
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (32, 32))
        cv2.putText(frame, f'{gesture}: {count}/100', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Capture', frame)
        key = cv2.waitKey(1)
        if key == 32:
            path = f'data/{gesture}/{gesture}_{count}.bmp'
            cv2.imwrite(path, resized)
            count += 1
            print(f'Saved {count}/100')
        elif key == ord('q'):
            print(f'Done with {gesture}')
            break

cv2.destroyAllWindows()
cap.release()
print("All done!")
