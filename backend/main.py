from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from inference import detect_objects
import shutil
import os

app = FastAPI()

UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    results = detect_objects(file_path, media_type="image")
    return JSONResponse(content=results)

@app.post("/upload/video/")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    results = detect_objects(file_path, media_type="video")
    return JSONResponse(content=results)
