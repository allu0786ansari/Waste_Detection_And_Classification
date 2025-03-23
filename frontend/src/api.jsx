import axios from "axios";

const API_BASE_URL = "http://localhost:8000";  // Change if needed

export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${API_BASE_URL}/upload/image`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
};

export const uploadVideo = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${API_BASE_URL}/upload/video`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
};
