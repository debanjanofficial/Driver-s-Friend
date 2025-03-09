import React, { useState, useMemo, useCallback } from 'react';
import { Box, Container, CssBaseline, ThemeProvider, createTheme, IconButton, Button } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import LogoutIcon from '@mui/icons-material/Logout';
import ChatWindow from './components/Chat/ChatWindow';
import LanguageSelector from './components/LanguageSelector/LanguageSelector';
import Login from './components/Auth/Login';
import { LanguageProvider } from './contexts/LanguageContext';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { Drawer, List, ListItem, ListItemButton, ListItemText, Typography, Divider, useMediaQuery, Avatar } from '@mui/material';

// Create AppContent component to use the auth hook inside the provider
const AppContent = () => {
  const { currentUser, logout } = useAuth();
  const [mode, setMode] = useState<'light' | 'dark'>('dark');
  const drawerWidth = 260;
  const exampleQueries = [
    "What's the speed limit in cities?",
    "Can I use my phone while driving?",
    "What's the alcohol limit for drivers?",
    "Do I need to use turn signals?"
  ];
  
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
  
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [activeQuery, setActiveQuery] = useState<string | null>(null);
  
  const handleQueryClick = useCallback((query: string) => {
    setActiveQuery(query);
  }, []);

  if (!currentUser) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box
          sx={{
            bgcolor: 'background.default',
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            p: 2
          }}
        >
          <Login />
        </Box>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <LanguageProvider>
        <Box
          sx={{
            bgcolor: 'background.default',
            minHeight: '100vh',
            display: 'flex',
          }}
        >
          {/* Sidebar */}
          <Drawer
            variant={isMobile ? "temporary" : "permanent"}
            open={!isMobile}
            sx={{
              width: drawerWidth,
              flexShrink: 0,
              [`& .MuiDrawer-paper`]: { 
                width: drawerWidth, 
                boxSizing: 'border-box',
                bgcolor: 'background.default',
                borderRight: 1,
                borderColor: 'divider'
              },
            }}
          >
            <Box sx={{ p: 2, display: 'flex', alignItems: 'center' }}>
              <Typography variant="h6" sx={{ fontWeight: 'bold', flexGrow: 1 }}>
                Driver's Friend
              </Typography>
            </Box>

            {/* User profile section */}
            <Box sx={{ p: 2, display: 'flex', alignItems: 'center' }}>
              <Avatar 
                src={currentUser?.photoURL || undefined} 
                alt={currentUser?.displayName || 'User'} 
                sx={{ mr: 2 }}
              />
              <Box>
                <Typography variant="body1" noWrap>
                  {currentUser?.displayName || 'User'}
                </Typography>
                <Typography variant="body2" color="text.secondary" noWrap>
                  {currentUser?.email || ''}
                </Typography>
              </Box>
            </Box>

            <Divider />
            <List>
              <ListItem>
                <Typography variant="overline" sx={{ opacity: 0.7 }}>
                  Example questions
                </Typography>
              </ListItem>
              {exampleQueries.map((query, index) => (
                <ListItemButton 
                  key={index}
                  onClick={() => handleQueryClick(query)}
                  sx={{
                    bgcolor: activeQuery === query ? 'action.selected' : 'transparent',
                    '&:hover': {
                      bgcolor: 'action.hover',
                    },
                  }}
                >
                  <ListItemText primary={query} />
                </ListItemButton>
              ))}
            </List>
            <Box sx={{ mt: 'auto', p: 2 }}>
              <Button
                fullWidth
                variant="outlined"
                color="inherit"
                startIcon={<LogoutIcon />}
                onClick={logout}
              >
                Sign Out
              </Button>
            </Box>
          </Drawer>

          {/* Main content */}
          <Box sx={{ 
            flexGrow: 1,
            ml: isMobile ? 0 : `${drawerWidth}px`, 
            transition: theme.transitions.create(['margin', 'width'], {
              easing: theme.transitions.easing.sharp,
              duration: theme.transitions.duration.leavingScreen,
            }),
            display: 'flex',
            flexDirection: 'column',
          }}>
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
            <Box sx={{ flexGrow: 1, p: 2 }}>
              <ChatWindow exampleQuery={activeQuery} />
            </Box>
          </Box>
        </Box>
      </LanguageProvider>
    </ThemeProvider>
  );
};

// Main App component with AuthProvider
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;