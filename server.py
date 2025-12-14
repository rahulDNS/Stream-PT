#!/usr/bin/env python3
"""
Edge-Streaming MJPEG Prototype
- Streams live MJPEG video from Mac camera to browser
- Supports snapshots
- Designed for network behavior testing (AP hopping, latency observation)
"""

import asyncio
import signal
from aiohttp import web
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor

CAMERA_INDEX = 0             # default Mac camera
JPEG_QUALITY = 80            # JPEG compression level
TARGET_FPS   = 20            # target FPS

capture = None
capture_lock = asyncio.Lock()
executor = ThreadPoolExecutor(max_workers=2)

async def ensure_camera():
    global capture
    async with capture_lock:
        if capture is None or not capture.isOpened():
            capture = cv2.VideoCapture(CAMERA_INDEX)
            await asyncio.sleep(0.1)
    return capture

def read_frame_jpeg():
    """
    Blocking camera read (runs in executor)
    Converts BGR → JPEG bytes
    """
    global capture
    if capture is None:
        return None
    ret, frame = capture.read()
    if not ret or frame is None:
        return None

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
    ok, jpg = cv2.imencode(".jpg", frame, encode_param)
    if not ok:
        return None
    return jpg.tobytes()


# ---------------- MJPEG STREAM ENDPOINT ----------------

async def mjpeg_stream(request):
    await ensure_camera()
    boundary = "frame"

    response = web.StreamResponse(
        status=200,
        reason="OK",
        headers={
            "Content-Type": f"multipart/x-mixed-replace; boundary=--{boundary}",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
    await response.prepare(request)

    interval = 1.0 / TARGET_FPS

    try:
        while True:
            jpg = await asyncio.get_event_loop().run_in_executor(
                executor, read_frame_jpeg
            )
            if jpg is None:
                await asyncio.sleep(0.05)
                continue

            part = (
                f"--{boundary}\r\n"
                "Content-Type: image/jpeg\r\n"
                f"Content-Length: {len(jpg)}\r\n\r\n"
            ).encode() + jpg + b"\r\n"

            await response.write(part)
            await asyncio.sleep(interval)

    except (asyncio.CancelledError, ConnectionResetError):
        pass

    return response


# ---------------- SNAPSHOT ENDPOINT ----------------

async def snapshot(request):
    await ensure_camera()
    jpg = await asyncio.get_event_loop().run_in_executor(executor, read_frame_jpeg)
    if jpg is None:
        return web.Response(status=503, text="Camera unavailable")
    return web.Response(body=jpg, content_type="image/jpeg")


# ---------------- ROUTES ----------------

routes = web.RouteTableDef()

@routes.get("/")
async def index(request):
    return web.FileResponse("static/index.html")

@routes.get("/style.css")
async def css(request):
    return web.FileResponse("static/style.css")

@routes.get("/stream")
async def stream_route(request):
    return await mjpeg_stream(request)

@routes.get("/snapshot")
async def snapshot_route(request):
    return await snapshot(request)

app = web.Application()
app.add_routes(routes)


# ---------------- CLEAN SHUTDOWN ----------------

def cleanup(loop):
    global capture
    if capture is not None:
        capture.release()
    executor.shutdown(wait=False)
    for task in asyncio.all_tasks(loop):
        task.cancel()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda: cleanup(loop))
        except NotImplementedError:
            pass

    web.run_app(app, port=8080)
