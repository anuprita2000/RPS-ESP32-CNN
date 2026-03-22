from camera import Camera

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
}

cam = Camera(**CAMERA_PARAMETERS)
cam.init()
cam.set_bmp_out(True)

# Capture and SAVE
cap = cam.capture()
with open("photo.bmp", "wb") as f:
    f.write(cap)

print("Saved! Bytes written:", len(cap))