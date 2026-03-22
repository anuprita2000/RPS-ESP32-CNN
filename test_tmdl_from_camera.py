import array
import gc
from image_preprocessing import resize_96x96_to_32x32_and_threshold
from image_preprocessing import strip_bmp_header
from camera import Camera, PixelFormat, FrameSize
import emlearn_cnn_fp32 as emlearn_cnn

MODEL = 'prs_cnn.tmdl'
RECOGNITION_THRESHOLD = 0.74

CAMERA_PARAMETERS = {
    "data_pins": [15, 17, 18, 16, 14, 12, 11, 48],
    "vsync_pin": 38,
    "href_pin": 47,
    "sda_pin": 40,
    "scl_pin": 39,
    "pclk_pin": 13,
    "xclk_pin": 10,
    "xclk_freq": 20000000,
    "powerdown_pin": -1,
    "reset_pin": -1,
    "frame_size": FrameSize.R96X96,
    "pixel_format": PixelFormat.GRAYSCALE
}

def argmax(values):
    return max(range(len(values)), key=lambda i: values[i])

classes = ['paper', 'rock', 'scissors']
current_prediction = classes[0]
cnt = 0

cam = Camera(**CAMERA_PARAMETERS)
cam.init()
cam.set_bmp_out(True)

with open(MODEL, 'rb') as f:
    model_data = array.array('B', f.read())
    print("Model Data Loaded..")
    gc.collect()
    model = emlearn_cnn.new(model_data)
    print("Model Loaded..")

print("Starting capture loop...")

while True:
    img = cam.capture()
    img = strip_bmp_header(img)
    img = resize_96x96_to_32x32_and_threshold(img)
    probabilities = [0.0, 0.0, 0.0]
    model.run(img, probabilities)
    out = argmax(probabilities)
    if probabilities[out] > RECOGNITION_THRESHOLD:
        prediction = classes[out]
        if prediction != current_prediction:
            current_prediction = prediction
            print(f"Prediction: {prediction} ({probabilities[out]:.2f})")
    cnt += 1