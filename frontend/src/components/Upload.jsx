import React, { useState } from "react";
import { uploadImage, uploadVideo } from "../api";

const Upload = ({ type }) => {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const uploadFn = type === "image" ? uploadImage : uploadVideo;
    const response = await uploadFn(file);
    setResults(response);
  };

  return (
    <div>
      <h2>Upload {type}</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>

      {results && <pre>{JSON.stringify(results, null, 2)}</pre>}
    </div>
  );
};

export default Upload;
