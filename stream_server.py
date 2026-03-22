# ── Rock Paper Scissors - ESP32 Stream Server ──
# Captures images from the OV3660 camera and streams them
# over WiFi to a laptop client for CNN classification.
# Author: Anuprita Kaple, Cornell MEM 5400, 2026

# Import required libraries
import socket
import network
from Wifi import Sta  # WiFi connection utility - Author: Sharil Tumin, MIT License
from camera import Camera, PixelFormat, FrameSize  # Camera driver - Seeed Studio

# Connect ESP32 to WiFi hotspot using credentials in Wifi.py
wif = Sta()
wif.connect()
wif.wait()

# Camera configuration parameters for XIAO ESP32-S3 Sense (OV3660)
# 96x96 resolution in grayscale - matches training image format
CAMERA_PARAMETERS = {
    "data_pins": [15, 17, 18, 16, 14, 12, 11, 48],  # GPIO pins for camera data
    "vsync_pin": 38,   # Vertical sync pin
    "href_pin": 47,    # Horizontal reference pin
    "sda_pin": 40,     # I2C data pin
    "scl_pin": 39,     # I2C clock pin
    "pclk_pin": 13,    # Pixel clock pin
    "xclk_pin": 10,    # External clock pin
    "xclk_freq": 20000000,  # 20MHz clock frequency
    "powerdown_pin": -1,    # Not used
    "reset_pin": -1,        # Not used
    "frame_size": FrameSize.R96X96,       # 96x96 pixel resolution
    "pixel_format": PixelFormat.GRAYSCALE  # Grayscale for CNN input
}

# Initialize camera with above parameters
cam = Camera(**CAMERA_PARAMETERS)
cam.init()
cam.set_bmp_out(True)  # Output images in BMP format including header

# Create a TCP socket server on port 5000
# ESP32 listens for an incoming connection from the laptop
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5000))  # Listen on all network interfaces
server.listen(1)  # Allow 1 connection at a time
print("Server waiting for connection on port 5000...")

# Accept connection from laptop client
conn, addr = server.accept()
print("Connected from", addr)

# Main loop - continuously capture and send images to laptop
while True:
    img = cam.capture()         # Capture one frame from camera
    size = len(img)             # Get image size in bytes
    conn.send(size.to_bytes(4, 'big'))  # Send 4-byte header with image size
    conn.send(img)              # Send the full image bytes