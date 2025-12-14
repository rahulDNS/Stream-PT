# Edge-Streaming (MJPEG Live Streaming Prototype)

A lightweight video streaming prototype built for experimenting with networking behavior, low-latency streaming, and Wi-Fi access-point handoff testing.  
This project uses a simple MJPEG pipeline to stream webcam frames from a Python server to a browser client.

This avoids complex codec dependencies and runs cleanly on macOS, Linux, or Raspberry Pi.

---

## Features

###  Live MJPEG video feed  
Continuous multipart JPEG streaming from the device camera to a browser.

###  Snapshot endpoint  
Instant capture of a single frame.

###  Low latency (~20–50ms typical)  
Easily tunable via FPS and JPEG quality.

###  Ideal for networking tests  
- Switching Wi-Fi networks (AP hopping)
- Nginx reverse proxy routing
- Observing frame drops, jitter, freeze time
- Measuring reconnect delay

###  Clean and portable  
No FFmpeg builds, no PyAV compilation, no WebRTC complexity.

---

## Project Structure

Edge-Streaming/
-server.py
-requirements.txt
-static/
  -index.html
  -style.css


---

## Installation


cd Edge-Streaming
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Run the Server
bash
Copy code
python3 server.py
Open:
http://localhost:8080

You will see:

Live MJPEG video feed

Snapshot button

Status display

---



In terminal:


cd Edge-Streaming
source venv/bin/activate
python3 server.py
Open browser → http://localhost:8080
You’ll see your live camera feed.



-------------------

Raspberry Pi Installation (Optional Future Setup)

If you want to run this streaming prototype on a Raspberry Pi, only a few additional steps are required:

Enable the Raspberry Pi Camera Module using sudo raspi-config


Go to Interface Options → Camera → Enable

we will have to reboot the Pi and install the required system dependencies

sudo apt update
sudo apt install python3-opencv python3-pip libatlas-base-dev


Clone the project

git clone https://github.com/<your-user>/<repo>
cd <repo>


Install Python dependencies

python3 -m venv venv
source venv/bin/activate
pip install aiohttp numpy
Run the streaming server
python3 server.py


View the stream from any device on the network

http://<pi-ip-address>:8080


This lets us run the same MJPEG streaming pipeline directly from a Raspberry Pi camera module, making the project portable across Mac, Linux, and embedded robotics environments.
