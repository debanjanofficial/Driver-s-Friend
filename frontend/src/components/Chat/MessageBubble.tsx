import React from 'react';
import { Box, Typography, Avatar, Chip, Link } from '@mui/material';
import { Message } from '../../types';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';
import PublicIcon from '@mui/icons-material/Public';
import DatabaseIcon from '@mui/icons-material/Storage';

interface Props {
    message: Message;
}

const MessageBubble: React.FC<Props> = ({ message }) => {
    const isBot = message.sender === 'bot';

    const getSourceIcon = (source?: string) => {
        if (source && (source.includes('.com') || source.includes('.info') || source.includes('.org'))) {
            return <PublicIcon sx={{ fontSize: 16 }} />;
        }
        return <DatabaseIcon sx={{ fontSize: 16 }} />;
    };

    const getSourceColor = (source?: string) => {
        if (source && (source.includes('.com') || source.includes('.info') || source.includes('.org'))) {
            return 'success';
        }
        return 'info';
    };

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
                        fontFamily: '"Söhne", ui-sans-serif, system-ui, -apple-system',
                        mb: message.source ? 1 : 0
                    }}
                >
                    {message.text}
                </Typography>
                
                {message.source && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                        <Chip
                            icon={getSourceIcon(message.source)}
                            label={message.source}
                            size="small"
                            color={getSourceColor(message.source)}
                            variant="outlined"
                            sx={{ fontSize: '0.75rem' }}
                        />
                        {message.url && (
                            <Link
                                href={message.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                sx={{ 
                                    fontSize: '0.75rem',
                                    color: 'primary.main',
                                    textDecoration: 'none',
                                    '&:hover': {
                                        textDecoration: 'underline'
                                    }
                                }}
                            >
                                View Source →
                            </Link>
                        )}
                    </Box>
                )}
            </Box>
        </Box>
    );
};

export default MessageBubble;
