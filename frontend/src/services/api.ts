import axios from 'axios';
import { ChatResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

export const chatAPI = {
    sendMessage: async (message: string, language: string): Promise<ChatResponse> => {
        try {
            const response = await axios.post(`${API_BASE_URL}/chat`, {
                message,
                language
            });
            return response.data;
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }
};