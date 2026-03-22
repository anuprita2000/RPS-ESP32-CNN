pythonfrom camera import Camera, PixelFormat, FrameSize

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

cam = Camera(**CAMERA_PARAMETERS)
cam.init()
cam.set_bmp_out(True)

img = cam.capture()

with open('test_image.bmp', 'wb') as f:
    f.write(img)

print("Image saved! Size:", len(img))