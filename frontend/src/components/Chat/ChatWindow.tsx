import React, { useState, useRef, useEffect } from 'react';
import { Box, Paper, Typography, CircularProgress } from '@mui/material';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';
import { useLanguage } from '../../contexts/LanguageContext';
import { chatAPI } from '../../services/api';
import { Message } from '../../types';

const ChatWindow: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isTyping, setIsTyping] = useState(false);
    const [isGenerating, setIsGenerating] = useState(false);
    const { language } = useLanguage();
    const messagesEndRef = useRef<null | HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(scrollToBottom, [messages, isTyping, isGenerating]);

    // Add a welcome message on initial load
    useEffect(() => {
        const welcomeMessage: Message = {
            id: 'welcome',
            text: 'Welcome to Driver\'s Friend! How can I help you with driving regulations today?',
            sender: 'bot',
            timestamp: new Date()
        };
        setMessages([welcomeMessage]);
    }, []);

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
            }, 100);
        });
    };

    const handleSendMessage = async (text: string) => {
        const userMessage: Message = {
            id: Date.now().toString(),
            text,
            sender: 'user',
            timestamp: new Date()
        };
        setMessages(prev => [...prev, userMessage]);

        setIsGenerating(true);

        try {
            const response = await chatAPI.sendMessage(text, language);
            const botMessage: Message = {
                id: (Date.now() + 1).toString(),
                text: '',
                sender: 'bot',
                timestamp: new Date()
            };
            setMessages(prev => [...prev, botMessage]);
            
            await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000));

            setIsGenerating(false);
            setIsTyping(true);
            await simulateTyping(response.response);
        } catch (error) {
            console.error('Error getting response:', error);
            setMessages(prev => [...prev, {
                id: (Date.now() + 1).toString(),
                text: 'Sorry, I encountered an error. Please try again later.',
                sender: 'bot',
                timestamp: new Date()
            }]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <Box sx={{ 
            display: 'flex', 
            flexDirection: 'column',
            height: 'calc(100vh - 80px)',
            position: 'relative'
        }}>
            <Box sx={{ 
                flexGrow: 1, 
                overflow: 'auto',
                mb: 10, // Space for the input box
                pb: 4
            }}>
                {messages.map(message => (
                    <MessageBubble key={message.id} message={message} />
                ))}
                
                {isGenerating && (
                    <Box sx={{ 
                        display: 'flex', 
                        p: 2, 
                        backgroundColor: 'background.paper',
                        borderTop: 1,
                        borderColor: 'divider',
                        alignItems: 'center',
                        gap: 2
                    }}>
                        <CircularProgress size={24} />
                        <Typography variant="body2">
                            Driver's Friend is thinking...
                        </Typography>
                    </Box>
                )}
                
                {isTyping && (
                    <Box sx={{ 
                        display: 'flex', 
                        p: 2, 
                        backgroundColor: 'background.paper',
                        borderTop: 1,
                        borderColor: 'divider',
                        alignItems: 'center',
                        gap: 2
                    }}>
                        <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                        <Typography variant="body2">
                            Driver's Friend is typing...
                        </Typography>
                    </Box>
                )}
                <div ref={messagesEndRef} />
            </Box>
            
            <ChatInput onSendMessage={handleSendMessage} />
        </Box>
    );
};

export default ChatWindow;