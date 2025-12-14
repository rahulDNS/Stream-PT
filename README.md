# Edge-Streaming (MJPEG Live Streaming Prototype)

A lightweight video streaming prototype built for experimenting with networking behavior, low-latency streaming, and Wi-Fi access-point handoff testing.  
This project uses a simple MJPEG pipeline to stream webcam frames from a Python server to a browser client.

This avoids complex codec dependencies and runs cleanly on macOS, Linux, or Raspberry Pi.

---

## Features

### ✓ Live MJPEG video feed  
Continuous multipart JPEG streaming from the device camera to a browser.

### ✓ Snapshot endpoint  
Instant capture of a single frame.

### ✓ Low latency (~20–50ms typical)  
Easily tunable via FPS and JPEG quality.

### ✓ Ideal for networking tests  
- Switching Wi-Fi networks (AP hopping)
- Nginx reverse proxy routing
- Observing frame drops, jitter, freeze time
- Measuring reconnect delay

### ✓ Clean and portable  
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

```bash
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

# ✔ RUNNING EVERYTHING

In terminal:

```bash
cd Edge-Streaming
source venv/bin/activate
python3 server.py
Open browser → http://localhost:8080
You’ll see your live camera feed.
