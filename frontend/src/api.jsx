const BASE_URL = "http://localhost:8000";

export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/upload/image/`, {
    method: "POST",
    body: formData,
  });

  return response.json();
};

export const uploadVideo = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/upload/video/`, {
    method: "POST",
    body: formData,
  });

  return response.json();
};
