import axios from 'axios';

const AUTH_API = 'http://localhost:8000/api/auth';

export const authService = {
    login: async (email: string, password: string) => {
        const response = await axios.post(`${AUTH_API}/login`, {
            email,
            password
        });
        return response.data;
    },
    
    register: async (email: string, password: string) => {
        const response = await axios.post(`${AUTH_API}/register`, {
            email,
            password
        });
        return response.data;
    }
};