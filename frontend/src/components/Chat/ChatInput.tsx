import React, { useState } from 'react';
import { Box, TextField, IconButton, Paper } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

interface Props {
    onSendMessage: (message: string) => void;
}

const ChatInput: React.FC<Props> = ({ onSendMessage }) => {
    const [message, setMessage] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (message.trim()) {
            onSendMessage(message);
            setMessage('');
        }
    };

    return (
        <Paper 
            component="form"
            onSubmit={handleSubmit}
            elevation={3}
            sx={{
                position: 'fixed',
                bottom: 30,
                left: '50%',
                transform: 'translateX(-50%)',
                width: '90%',
                maxWidth: '800px',
                display: 'flex',
                p: 1,
                borderRadius: 2
            }}
        >
            <TextField
                fullWidth
                multiline
                maxRows={4}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Message Driver's Friend..."
                variant="outlined"
                sx={{
                    '& .MuiOutlinedInput-root': {
                        borderRadius: 2,
                        fontSize: '0.9rem',
                    }
                }}
            />
            <IconButton 
                type="submit" 
                color="primary" 
                sx={{ 
                    ml: 1,
                    alignSelf: 'flex-end'
                }}
            >
                <SendIcon />
            </IconButton>
        </Paper>
    );
};

export default ChatInput;