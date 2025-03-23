import React, { useState } from "react";
import { uploadVideo } from "../api";

const UploadVideo = () => {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const response = await uploadVideo(file);
    setResults(response);
  };

  return (
    <div className="upload-container">
      <h2 className="upload-title">Upload Your Video</h2>
      <p className="upload-description">
        Import your video file to detect and classify
      </p>

      <input
        type="file"
        accept="video/*"
        onChange={handleFileChange}
        className="file-input"
      />

      <button className="upload-btn" onClick={handleUpload} disabled={!file}>
        Upload Video
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

export default UploadVideo;
