import React from 'react';
import { Box, Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import ChatWindow from './components/Chat/ChatWindow';
import LanguageSelector from './components/LanguageSelector/LanguageSelector';
import { LanguageProvider } from './contexts/LanguageContext';

const theme = createTheme();

function App() {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <LanguageProvider>
                <Container>
                    <Box sx={{ py: 4 }}>
                        <LanguageSelector />
                        <ChatWindow />
                    </Box>
                </Container>
            </LanguageProvider>
        </ThemeProvider>
    );
}

export default App;