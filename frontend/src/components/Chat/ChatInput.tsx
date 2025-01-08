import React, { useState } from 'react';
import { Box, TextField, IconButton } from '@mui/material';
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
        <Box
            component="form"
            onSubmit={handleSubmit}
            sx={{
                p: 2,
                borderTop: 1,
                borderColor: 'divider',
                display: 'flex'
            }}
        >
            <TextField
                fullWidth
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your message..."
                variant="outlined"
                size="small"
            />
            <IconButton type="submit" color="primary" sx={{ ml: 1 }}>
                <SendIcon />
            </IconButton>
        </Box>
    );
};

export default ChatInput;