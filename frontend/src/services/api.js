import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getHealthData = async () => {
  const response = await api.get("/analyze");
  return response.data;
};

export const uploadCSV = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export default api;