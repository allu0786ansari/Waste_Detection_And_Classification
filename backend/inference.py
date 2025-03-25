'''
No need to use inference.py if we are using model.pt format

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
import cv2
import numpy as np
import openvino as ov
from io import BytesIO
from pathlib import Path


# Load OpenVINO model
MODEL_PATH = "models/best_model_waste_detection.xml"
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


def detect_from_image(image):
    """Preprocess image, run inference, and draw bounding boxes."""

    # Resize image to match model input shape
    h, w = image.shape[:2]
    input_shape = (640, 640)  # Update this based on your model's expected input size
    resized_image = cv2.resize(image, input_shape)  # Resize to match model input size

    # Convert image to match model input format
    input_blob = np.expand_dims(resized_image.transpose(2, 0, 1), axis=0)  # [1, C, H, W]
    input_blob = input_blob.astype(np.float32) / 255.0  # Normalize if required by model


    # Perform inference
    results = compiled_model([input_blob])[0]  

    # Check if detections exist
    if results is None or results.shape[1] == 0:
        print("No objects detected!")
        return image  # Return original image if no objects found

    # Loop through detections
    for detection in results[0]:  # Assuming output shape [1, num_detections, 6]
        conf = detection[4]  # Confidence score
        if conf > 0.1:  # Adjust confidence threshold if needed
            x_center, y_center, width, height = detection[:4]
            x_min = int((x_center - width / 2) * w)
            y_min = int((y_center - height / 2) * h)
            x_max = int((x_center + width / 2) * w)
            y_max = int((y_center + height / 2) * h)

            class_id = int(detection[5])
            class_label = CLASS_LABELS[class_id] if class_id < len(CLASS_LABELS) else "unknown"

            #Draw bounding box
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(image, f"{class_label} ({conf:.2f})", (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image  #Return image with bounding boxes
'''
