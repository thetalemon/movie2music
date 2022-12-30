import axios from 'axios';
import axiosRetry from 'axios-retry';

export const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000/',
  responseType: 'json',
  headers: {
    'Content-Type': 'application/json',
  },
});

axiosRetry(apiClient, { retries: 5, retryDelay: axiosRetry.exponentialDelay });
