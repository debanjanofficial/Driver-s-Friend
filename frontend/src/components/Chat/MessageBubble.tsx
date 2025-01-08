import React from 'react';
import { Box, Typography } from '@mui/material';
import { Message } from '../../types';

interface Props {
    message: Message;
}

const MessageBubble: React.FC<Props> = ({ message }) => {
    const isBot = message.sender === 'bot';

    return (
        <Box
            sx={{
                display: 'flex',
                justifyContent: isBot ? 'flex-start' : 'flex-end',
                mb: 2
            }}
        >
            <Box
                sx={{
                    maxWidth: '70%',
                    backgroundColor: isBot ? 'primary.light' : 'secondary.light',
                    borderRadius: 2,
                    p: 2
                }}
            >
                <Typography variant="body1">{message.text}</Typography>
                <Typography variant="caption" sx={{ opacity: 0.7 }}>
                    {message.timestamp.toLocaleTimeString()}
                </Typography>
            </Box>
        </Box>
    );
};

export default MessageBubble;