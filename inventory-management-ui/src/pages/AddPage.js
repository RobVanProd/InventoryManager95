import React from 'react';
import { Typography, TextField, Button, Box } from '@mui/material';

function AddPage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>Add New Item</Typography>
      <form>
        <TextField label="Item Name" variant="outlined" fullWidth margin="normal" />
        <TextField label="Quantity" variant="outlined" fullWidth margin="normal" />
        <Button variant="contained" color="primary" type="submit">Add Item</Button>
      </form>
    </Box>
  );
}

export default AddPage;
