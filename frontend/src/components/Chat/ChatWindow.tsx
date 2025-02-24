import React, { useState, useRef, useEffect } from 'react';
import { Box, Paper, Button, Typography} from '@mui/material';
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
    const [isTyping, setIsTyping] = useState(false);
    const [isGenerating, setIsGenerating] = useState(false);
    const { language } = useLanguage();
    const messagesEndRef = useRef<null | HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(scrollToBottom, [messages]);

    const simulateTyping = (text: string) => {
        return new Promise<void>((resolve) => {
            const words = text.split(' ');
            let currentText = '';
            let index = 0;

            const interval = setInterval(() => {
                if (index < words.length) {
                    currentText += words[index] + ' ';
                    setMessages(prev => {
                        const lastMessage = prev[prev.length - 1];
                        if (lastMessage && lastMessage.sender === 'bot') {
                            lastMessage.text = currentText;
                            return [...prev.slice(0, -1), lastMessage];
                        }
                        return prev;
                    });
                    index++;
                } else {
                    clearInterval(interval);
                    resolve();
                }
            }, 100); // Adjust typing speed here
        });
    };

    const handleSendMessage = async (text: string) => {
        // Add user message
        const userMessage: Message = {
            id: Date.now().toString(),
            text,
            sender: 'user',
            timestamp: new Date()
        };
        setMessages(prev => [...prev, userMessage]);

        setIsGenerating(true);

        try {
            // Get bot response
            const response = await chatAPI.sendMessage(text, language);
            const botMessage: Message = {
                id: (Date.now() + 1).toString(),
                text: '',
                sender: 'bot',
                timestamp: new Date()
            };
            setMessages(prev => [...prev, botMessage]);
            // Wait for 2-3 seconds before starting to type
            await new Promise(resolve => setTimeout(resolve, 2000 + Math.random() * 1000));

            setIsGenerating(false);
            setIsTyping(true);
            await simulateTyping(response.response);
        } catch (error) {
            console.error('Error getting response:', error);
        } finally {
            setIsTyping(false);
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
                {isGenerating && (
                    <Typography variant="body2" sx={{ color: 'gray', fontStyle: 'italic' }}>
                        Driver's Friend is generating answer...
                    </Typography>
                )}
                {isTyping && (
                    <Typography variant="body2" sx={{ color: 'gray', fontStyle: 'italic' }}>
                        Driver's Friend is typing...
                    </Typography>
                )}
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