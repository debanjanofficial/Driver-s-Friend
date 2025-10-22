export interface Message {
    id: string;
    text: string;
    sender: 'user' | 'bot';
    timestamp: Date;
    source?: string;
    url?: string;
}

export interface ChatResponse {
    response: string;
    intent: string;
    confidence: number;
    search_results?: any[];
    suggestions?: string[];
    source?: string;
    url?: string;
}
