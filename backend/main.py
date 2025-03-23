from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import shutil
import os
import cv2

from fastapi.middleware.cors import CORSMiddleware  # ✅ Make sure this is imported

from inference import detect_from_image

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow requests from React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    """Handles image upload, processes it with object detection, and returns the processed image."""
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read image and detect objects
    image = cv2.imread(file_path)

    if image is None:
        print("Error loading image:", file_path)
        return Response(content="Failed to load image", media_type="text/plain", status_code=400)
    
    processed_image = detect_from_image(image)

    # Encode image for response
    _, buffer = cv2.imencode(".png", processed_image)
    return Response(content=buffer.tobytes(), media_type="image/png")


