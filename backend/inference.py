from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import openvino as ov
from pathlib import Path
import shutil
import json

app = FastAPI()

# Load OpenVINO model
MODEL_PATH = "models/best_model_waste_detection.xml"  # Path to FP16 or FP32 model
core = ov.Core()
model = core.read_model(MODEL_PATH)
compiled_model = core.compile_model(model, "CPU")

# Class labels (update with actual labels from your dataset)
CLASS_LABELS = [
    "Food cup -ice or yoghurt- including caps",
    "Food bowl or pizza box",
    "Snacks-bags take away food package",
    "Napkin -food_take away-",
    "Wrap-sack-stick",
    "Tin Can",
    "Small drinking cup -Coffee-tea-",
    "Smoking pack and material",
    "Receipts",
    "Nose-mouth masks"
]

def detect_objects(file_path, media_type="image"):
    if media_type == "image":
        return detect_from_image(file_path)
    elif media_type == "video":
        return detect_from_video(file_path)

def detect_from_image(image_path):
    image = cv2.imread(image_path)
    h, w = image.shape[:2]

    input_blob = np.expand_dims(image.transpose(2, 0, 1), axis=0)
    result = compiled_model([input_blob])[0]

    boxes, scores, labels = [], [], []
    for detection in result[0]:  # [1, num_detections, 6]
        conf = detection[4]
        if conf > 0.4:
            x_center, y_center, width, height = detection[:4]
            x_min = int((x_center - width / 2) * w)
            y_min = int((y_center - height / 2) * h)
            x_max = int((x_center + width / 2) * w)
            y_max = int((y_center + height / 2) * h)

            class_id = int(detection[5])
            class_label = CLASS_LABELS[class_id] if class_id < len(CLASS_LABELS) else "unknown"

            boxes.append([x_min, y_min, x_max, y_max])
            scores.append(float(conf))
            labels.append(class_label)

    return {"boxes": boxes, "scores": scores, "labels": labels}

def detect_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    results = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        h, w = frame.shape[:2]
        input_blob = np.expand_dims(frame.transpose(2, 0, 1), axis=0)
        result = compiled_model([input_blob])[0]

        frame_results = []
        for detection in result[0]:  # [1, num_detections, 6]
            conf = detection[4]
            if conf > 0.4:
                x_center, y_center, width, height = detection[:4]
                x_min = int((x_center - width / 2) * w)
                y_min = int((y_center - height / 2) * h)
                x_max = int((x_center + width / 2) * w)
                y_max = int((y_center + height / 2) * h)

                class_id = int(detection[5])
                class_label = CLASS_LABELS[class_id] if class_id < len(CLASS_LABELS) else "unknown"

                frame_results.append({"box": [x_min, y_min, x_max, y_max], "label": class_label, "score": conf})
        
        results.append(frame_results)

    cap.release()
    return {"frames": results}