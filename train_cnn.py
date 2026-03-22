import numpy as np
from PIL import Image
import os
import tensorflow as tf
from tensorflow import keras

# Load images
X = []
y = []
classes = ['rock', 'paper', 'scissors']

for label, gesture in enumerate(classes):
    folder = f'data/{gesture}'
    for fname in os.listdir(folder):
        if fname.endswith('.bmp'):
            img = Image.open(f'{folder}/{fname}').convert('L')
            img = img.resize((32, 32))
            X.append(np.array(img))
            y.append(label)

X = np.array(X).reshape(-1, 32, 32, 1) / 255.0
y = np.array(y)

print(f"Total images: {len(X)}")

# Build CNN
model = keras.Sequential([
    keras.layers.Input((32, 32, 1)),
    keras.layers.Conv2D(8, 3, activation='relu'),
    keras.layers.MaxPooling2D(),
    keras.layers.Conv2D(16, 3, activation='relu'),
    keras.layers.MaxPooling2D(),
    keras.layers.Flatten(),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

# Train
model.fit(X, y, epochs=30, validation_split=0.2)

# Save
model.save('prs_cnn.h5')
print("Model saved as prs_cnn.h5")
