import axios from "axios";

export const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8080/",
  responseType: "json",
  headers: {
    "Content-Type": "application/json",
  },
});