import React from 'react';
import { Box, Typography, Avatar } from '@mui/material';
import { Message } from '../../types';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';

interface Props {
    message: Message;
}

const MessageBubble: React.FC<Props> = ({ message }) => {
    const isBot = message.sender === 'bot';

    return (
        <Box
            sx={{
                display: 'flex',
                width: '100%',
                p: 2,
                backgroundColor: isBot ? 'background.paper' : 'background.default',
                borderTop: 1,
                borderColor: 'divider',
                alignItems: 'flex-start',
                gap: 2
            }}
        >
            <Avatar sx={{ 
                bgcolor: isBot ? 'primary.main' : 'secondary.main',
                width: 36,
                height: 36
            }}>
                {isBot ? <SmartToyIcon /> : <PersonIcon />}
            </Avatar>
            <Box sx={{ flexGrow: 1 }}>
                <Typography 
                    variant="body1" 
                    sx={{ 
                        whiteSpace: 'pre-wrap',
                        fontFamily: '"Söhne", ui-sans-serif, system-ui, -apple-system'
                    }}
                >
                    {message.text}
                </Typography>
            </Box>
        </Box>
    );
};

export default MessageBubble;