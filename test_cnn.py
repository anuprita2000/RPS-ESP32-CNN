import cv2
import numpy as np
from tensorflow import keras

model = keras.models.load_model('prs_cnn.h5')
classes = ['rock', 'paper', 'scissors']

cap = cv2.VideoCapture(0)
print("Show your hand to the camera. Press Q to quit.")

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (32, 32))
    
    img = resized.reshape(1, 32, 32, 1) / 255.0
    pred = model.predict(img, verbose=0)
    label = classes[np.argmax(pred)]
    confidence = np.max(pred) * 100
    
    cv2.putText(frame, f'{label} ({confidence:.0f}%)', 
                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                1.5, (0, 255, 0), 3)
    cv2.imshow('Rock Paper Scissors', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

