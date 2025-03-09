import React from 'react';
import { Box, Button, Typography, Paper } from '@mui/material';
import GoogleIcon from '@mui/icons-material/Google';
import { useAuth } from '../../contexts/AuthContext';

const Login: React.FC = () => {
  const { signInWithGoogle } = useAuth();

  return (
    <Paper
      elevation={3}
      sx={{
        p: 4,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        maxWidth: '400px',
        margin: '0 auto',
        mt: 4
      }}
    >
      <Typography variant="h5" component="h1" gutterBottom>
        Welcome to Driver's Friend
      </Typography>
      <Typography variant="body1" sx={{ mb: 3 }}>
        Sign in to access personalized driving assistance
      </Typography>
      <Button
        variant="contained"
        startIcon={<GoogleIcon />}
        onClick={signInWithGoogle}
        fullWidth
        sx={{ 
          backgroundColor: '#fff', 
          color: '#444', 
          border: '1px solid #ddd',
          '&:hover': { 
            backgroundColor: '#f1f1f1' 
          },
          mb: 2
        }}
      >
        Sign in with Google
      </Button>
    </Paper>
  );
};

export default Login;