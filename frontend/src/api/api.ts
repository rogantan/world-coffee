import axios from 'axios'
// import { error } from 'console';
import router from '../router/index'

const apiClient = axios.create({
    baseURL: "http://127.0.0.1:14325/backend",
    headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json',
    }
});

apiClient.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            router.push('/signin');
        }
        return Promise.reject(error);
    }
);

apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (config.data instanceof FormData) {
        config.headers['Content-Type'] = 'multipart/form-data';
    }
    if (config.url && config.url.includes('/token')) {
        config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
    } else if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export const apiService = {
    async get<T>(url: string, params?: object): Promise<T> {
        try {
            const response = await apiClient.get(url, params);
            return response.data;
        } catch (error) {
            console.error('GET request error', error);
            throw error;
        }
    },

    async post<T>(url: string, data?: object): Promise<T> {
        try {
            const response = await apiClient.post(url, data);
            return response.data;
        } catch (error) {
            console.log('POST request error', error);
            throw error;
        }
    },

    async put<T>(url: string, data?: object): Promise<T> {
        try {
            const response = await apiClient.put(url, data);
            return response.data;
        } catch (error) {
            console.error('POST request error', error);
            throw error;
        }
    },

    async delete<T>(url: string): Promise<T> {
        try {
            const response = await apiClient.delete(url);
            return response.data;
        } catch (error) {
            console.log('DELETE request error', error);
            throw error;
        }
    },
};