import React, { useState } from "react";
import { uploadImage } from "../api";

const UploadImage = () => {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const response = await uploadImage(file);
    setResults(response);
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

      {results && (
        <div className="results-container">
          <h3>Detection Results:</h3>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default UploadImage;
