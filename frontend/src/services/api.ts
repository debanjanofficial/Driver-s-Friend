import axios from 'axios';
import { ChatResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';


interface SearchParams {
    query: string;
    language: string;
    category?: string;
    limit?: number;
}

interface SearchResponse {
    results: any[];
    query: string;
    matched_keywords: string[];
    total_results: number;
}

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
    },

    search: async (params: SearchParams): Promise<SearchResponse> => {
        try {
            const response = await axios.post(`${API_BASE_URL}/search`, params);
            return response.data;
        } catch (error) {
            console.error('Error searching:', error);
            throw error;
        }
    },

    getCategories: async (language: string): Promise<string[]> => {
        try {
            const response = await axios.get(`${API_BASE_URL}/categories`, {
                params: { language }
            });
            return response.data.categories;
        } catch (error) {
            console.error('Error fetching categories:', error);
            throw error;
        }
    }
};