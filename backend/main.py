from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import shutil
import os
import cv2
import numpy as np
import torch
from ultralytics import YOLO

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust if frontend runs elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLOv8 model (.pt) directly
model = YOLO("models/best_model_waste_detection.pt")

UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    """Handles image upload, runs object detection, and returns the processed image."""

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read and process image
    image = cv2.imread(file_path)

    if image is None:
        print(f"Error loading image: {file_path}")
        return Response(content="Failed to load image", media_type="text/plain", status_code=400)

    print(f"Image loaded successfully: {file_path}")

    # Convert BGR (OpenCV) to RGB format
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Run detection using the YOLOv8 model
    results = model(image_rgb)

    # Get the image with bounding boxes
    detected_img = results[0].plot()

    # Convert back to PNG format
    _, buffer = cv2.imencode(".png", detected_img)

    return Response(content=buffer.tobytes(), media_type="image/png")
