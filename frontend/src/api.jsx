import axios from "axios";

const API_URL = "http://localhost:8000";  // Update if backend runs on a different port

export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(`${API_URL}/upload/image/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
      responseType: "blob", 
    });

    return response.data; 
  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
};
