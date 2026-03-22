# RPS-ESP32-CNN

A real-time **Rock Paper Scissors (RPS)** classifier using an **ESP32-CAM** module and a **Convolutional Neural Network (CNN)** trained in Python.

## Project Overview

This project streams live camera images from an ESP32-CAM to a laptop, where a trained CNN model classifies hand gestures as Rock, Paper, or Scissors in real time.

## Repository Structure

### Laptop Scripts
| File | Description |
|------|-------------|
| `train_esp.py` | Train CNN model on ESP32-captured images |
| `train_cnn.py` | General CNN training script |
| `test_cnn.py` | Test/evaluate the trained model |
| `classify_stream.py` | Real-time classification from ESP32 stream |
| `receive_stream.py` | Receive and display the video stream |
| `collect_from_esp.py` | Collect training images from ESP32 |
| `collect_images.py` | General image collection utility |
| `collect_paper.py` | Collect images for the "Paper" class |
| `prs_cnn_esp.h5` | Trained CNN model (ESP32-optimized) |

### ESP32 Scripts (on device)
| File | Description |
|------|-------------|
| `stream_server.py` | MicroPython HTTP stream server on ESP32-CAM |
| `camera_test.py` | Test ESP32 camera functionality |
| `capturetest.py` | Capture test images from ESP32 |
| `Wifi.py` | WiFi connection helper for ESP32 |
| `image_preprocessing.py` | On-device image preprocessing |

## Setup

1. Flash MicroPython to the ESP32-CAM and upload ESP32 scripts.
2. Connect ESP32 to your WiFi network.
3. Run `stream_server.py` on the ESP32.
4. On your laptop, run `classify_stream.py` to start real-time RPS classification.

## Model

- Framework: TensorFlow / Keras
- Input: Images streamed from ESP32-CAM
- Output: Rock / Paper / Scissors classification
- Model file: `prs_cnn_esp.h5`

## Author

Anuprita Kaple (ak2837)
