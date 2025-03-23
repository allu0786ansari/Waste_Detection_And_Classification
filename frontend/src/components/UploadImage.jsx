import React, { useState } from "react";
import { uploadImage } from "../api";
import './style.css';

const UploadImage = () => {
  const [file, setFile] = useState(null);
  const [imageSrc, setImageSrc] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null); // Clear previous errors
  };

  const handleUpload = async () => {
    if (!file) return;

    try {
      const blob = await uploadImage(file); // Receive image as Blob
      const imageUrl = URL.createObjectURL(blob); // Convert Blob to URL
      setImageSrc(imageUrl);
    } catch (error) {
      console.error("Error uploading image:", error);
      setError("Failed to process image. Please try again.");
    }
  };

  return (
    <div className="upload-container">
      <h2 className="upload-title">Upload Your Image</h2>
      <p className="upload-description">
        Import your image file to detect and classify
      </p>

      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="file-input"
      />

      <button className="upload-btn" onClick={handleUpload} disabled={!file}>
        Upload Image
      </button>

      {error && <p className="error-message">{error}</p>}

      {imageSrc && (
        <div className="results-container">
          <h3>Detection Results:</h3>
          <img src={imageSrc} alt="Detected Image" className="detected-image" />
        </div>
      )}
    </div>
  );
};

export default UploadImage;
