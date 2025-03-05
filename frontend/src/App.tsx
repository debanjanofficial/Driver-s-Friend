import React, { useState, useMemo } from 'react';
import { Box, Container, CssBaseline, ThemeProvider, createTheme, IconButton } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import ChatWindow from './components/Chat/ChatWindow';
import LanguageSelector from './components/LanguageSelector/LanguageSelector';
import { LanguageProvider } from './contexts/LanguageContext';

function App() {
    const [mode, setMode] = useState<'light' | 'dark'>('dark');
    
    const theme = useMemo(
        () =>
            createTheme({
                palette: {
                    mode,
                    primary: {
                        main: mode === 'dark' ? '#10a37f' : '#10a37f',
                    },
                    secondary: {
                        main: mode === 'dark' ? '#5436DA' : '#5436DA',
                    },
                    background: {
                        default: mode === 'dark' ? '#343541' : '#ffffff',
                        paper: mode === 'dark' ? '#444654' : '#f7f7f8',
                    },
                },
            }),
        [mode],
    );

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <LanguageProvider>
                <Box
                    sx={{
                        bgcolor: 'background.default',
                        minHeight: '100vh',
                        display: 'flex',
                        flexDirection: 'column'
                    }}
                >
                    <Box sx={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        p: 2, 
                        borderBottom: 1, 
                        borderColor: 'divider' 
                    }}>
                        <LanguageSelector />
                        <IconButton onClick={() => setMode(mode === 'dark' ? 'light' : 'dark')} color="inherit">
                            {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
                        </IconButton>
                    </Box>
                    <Container maxWidth="md" sx={{ flexGrow: 1, py: 4 }}>
                        <ChatWindow />
                    </Container>
                </Box>
            </LanguageProvider>
        </ThemeProvider>
    );
}

export default App;