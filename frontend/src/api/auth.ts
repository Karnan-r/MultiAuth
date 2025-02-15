import axios from "axios";

const API_URL = "http://127.0.0.1:5000/api";
const BACKEND_URL = "http://127.0.0.1:5000"; // Make sure this matches your backend

// 🔹 Signup API
export const signup = async (name: string, email: string, password: string, tenantName: string) => {
  return axios.post(`${API_URL}/signup`, { name, email, password, tenant_name: tenantName });
};

// 🔹 Login API
export const login = async (email: string, password: string) => {
  const res = await axios.post(`${API_URL}/login`, { email, password });
  localStorage.setItem("jwt", res.data.access_token); // Store JWT
  return res.data;
};

// 🔹 Fetch User Data (GET /api/me)
export const getUser = async () => {
  const token = localStorage.getItem("jwt");
  return axios.get(`${API_URL}/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });
};

// 🔹 Fetch Users (Admin Only)
export const getUsers = async () => {
  const token = localStorage.getItem("jwt");
  return axios.get(`${API_URL}/users`, {
    headers: { Authorization: `Bearer ${token}` }
  });
};

// 🔹 Start Google Login
export const googleLogin = () => {
  window.location.href = `${BACKEND_URL}/login/google`;
};

// 🔹 Handle Google OAuth Callback (Extract Token)
export const handleGoogleCallback = async (token: string) => {
  const res = await axios.get(`${API_URL}/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  localStorage.setItem("jwt", token);
  return res.data;
};
