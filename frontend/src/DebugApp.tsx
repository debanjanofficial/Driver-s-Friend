import React from 'react';
import { Box, Typography, Button } from '@mui/material';

const DebugApp: React.FC = () => {
  const [count, setCount] = React.useState(0);

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h3" gutterBottom>
        🚗 Driver's Friend Debug
      </Typography>
      <Typography variant="body1" gutterBottom>
        React is working! Count: {count}
      </Typography>
      <Button 
        variant="contained" 
        onClick={() => setCount(c => c + 1)}
        sx={{ mr: 2 }}
      >
        Test Button
      </Button>
      <Button 
        variant="outlined" 
        onClick={() => {
          fetch('http://localhost:8000/api/health')
            .then(res => res.json())
            .then(data => alert(`Backend Status: ${data.status}`))
            .catch(err => alert(`Error: ${err.message}`));
        }}
      >
        Test Backend
      </Button>
    </Box>
  );
};

export default DebugApp;