import React from 'react';
import { Typography } from '@mui/material';

function HomePage() {
  return (
    <div>
      <Typography variant="h4" component="h1" gutterBottom>
        Welcome to Inventory Management
      </Typography>
      <Typography variant="body1">
        This is the home page.
      </Typography>
    </div>
  );
}

export default HomePage;
