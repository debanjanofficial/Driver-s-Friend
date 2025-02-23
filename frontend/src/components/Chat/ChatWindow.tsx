import React, { useState, useRef, useEffect } from 'react';
import { Box, Paper, Button } from '@mui/material';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';
import { useLanguage } from '../../contexts/LanguageContext';
import { chatAPI } from '../../services/api';
import { Message } from '../../types';
import { useTranslation } from 'react-i18next';

const ChatMessage = ({ intent }: { intent: string }) => {
    const { t } = useTranslation();

    return (
        <div>
            <p>{t(intent)}</p>
        </div>
    );
};

const ChatWindow: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const { language } = useLanguage();
    const messagesEndRef = useRef<null | HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSendMessage = async (text: string) => {
        // Add user message
        const userMessage: Message = {
            id: Date.now().toString(),
            text,
            sender: 'user',
            timestamp: new Date()
        };
        setMessages(prev => [...prev, userMessage]);

        try {
            // Get bot response
            const response = await chatAPI.sendMessage(text, language);
            const botMessage: Message = {
                id: (Date.now() + 1).toString(),
                text: response.response,
                sender: 'bot',
                timestamp: new Date()
            };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error('Error getting response:', error);
        }
    };
    const handleClearChat = () => {
        setMessages([]);
    };

    return (
        <Paper elevation={3} sx={{ height: '80vh', maxWidth: '600px', margin: 'auto' }}>
            <Box sx={{ height: '90%', overflow: 'auto', p: 2 }}>
                {messages.map(message => (
                    <MessageBubble key={message.id} message={message} />
                ))}
                <div ref={messagesEndRef} />
            </Box>
            <Box sx ={{ display: 'flex', justifyContent: 'space-between', pb: 2 }}>
                <Button variant="contained" color="secondary" onClick={handleClearChat}>
                    Clear Chat
                </Button>
            <ChatInput onSendMessage={handleSendMessage} />
            </Box>
        </Paper>
    );
};

export default ChatWindow;