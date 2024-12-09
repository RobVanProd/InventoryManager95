import React, { useState, useEffect } from 'react';
import {
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Alert,
  Box,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import { inventoryApi } from '../services/api';
import Notification from '../components/Notification';

function ViewPage() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState('');
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'success' });

  const fetchItems = async () => {
    try {
      const response = await inventoryApi.getItems();
      setItems(response.data);
    } catch (error) {
      console.error('Error fetching items:', error);
      setError('Failed to load inventory items. Please try again.');
    }
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const handleDelete = async (id) => {
    try {
      await inventoryApi.deleteItem(id);
      setNotification({ open: true, message: 'Item deleted successfully', severity: 'success' });
      fetchItems(); // Refresh the list
    } catch (error) {
      console.error('Error deleting item:', error);
      setNotification({ open: true, message: 'Failed to delete item', severity: 'error' });
    }
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 1200, mx: 'auto', mt: 3 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Inventory Items
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell align="right">Quantity</TableCell>
              <TableCell>Description</TableCell>
              <TableCell align="right">Price</TableCell>
              <TableCell>Warehouse</TableCell>
              <TableCell>Sub-Warehouse</TableCell>
              <TableCell align="center">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {items.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} align="center">
                  <Typography variant="body1" sx={{ py: 2 }}>
                    No items found. Add some items to see them here.
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              items.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.name}</TableCell>
                  <TableCell align="right">{item.quantity}</TableCell>
                  <TableCell>{item.description || '-'}</TableCell>
                  <TableCell align="right">
                    {item.price ? `$${parseFloat(item.price).toFixed(2)}` : '-'}
                  </TableCell>
                  <TableCell>{item.warehouse_name || '-'}</TableCell>
                  <TableCell>{item.subwarehouse_name || '-'}</TableCell>
                  <TableCell align="center">
                    <IconButton
                      color="primary"
                      onClick={() => console.log('Edit item', item.id)}
                      size="small"
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      color="error"
                      onClick={() => handleDelete(item.id)}
                      size="small"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Notification
        open={notification.open}
        message={notification.message}
        severity={notification.severity}
        onClose={handleCloseNotification}
      />
    </Paper>
  );
}

export default ViewPage;
