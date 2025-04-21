import axios from "axios";

// Create an Axios instance
const api = axios.create({
  baseURL: "http://127.0.0.1:5000", // Your backend URL
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

// Add request interceptor to attach token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("jwt_token"); // Retrieve token
    console.log("🔵 Sending Authorization Header:", token);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`; // Attach token
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 Unauthorized errors (Token Expired)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.warn("Session expired. Logging out...");
      localStorage.removeItem("jwt_token"); // Remove token
      localStorage.removeItem("user_id");
      localStorage.removeItem("user_type");
      window.location.href = "/login"; // Redirect to login
    }
    return Promise.reject(error);
  }
);

export default api;
