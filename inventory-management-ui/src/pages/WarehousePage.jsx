import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import { inventoryApi } from '../services/api';
import Notification from '../components/Notification';

function WarehousePage() {
  const [warehouses, setWarehouses] = useState([]);
  const [formData, setFormData] = useState({ name: '', location: '' });
  const [editingId, setEditingId] = useState(null);
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'success' });
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    fetchWarehouses();
  }, []);

  const fetchWarehouses = async () => {
    try {
      const response = await inventoryApi.getWarehouses();
      setWarehouses(response.data);
    } catch (error) {
      showNotification('Error fetching warehouses', 'error');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await inventoryApi.updateWarehouse(editingId, formData);
        showNotification('Warehouse updated successfully');
      } else {
        await inventoryApi.createWarehouse(formData);
        showNotification('Warehouse created successfully');
      }
      setFormData({ name: '', location: '' });
      setEditingId(null);
      fetchWarehouses();
    } catch (error) {
      showNotification(error.response?.data?.message || 'Error saving warehouse', 'error');
    }
  };

  const handleEdit = (warehouse) => {
    setFormData({ name: warehouse.name, location: warehouse.location });
    setEditingId(warehouse.id);
    setDialogOpen(true);
  };

  const handleDelete = async (id) => {
    try {
      await inventoryApi.deleteWarehouse(id);
      showNotification('Warehouse deleted successfully');
      fetchWarehouses();
    } catch (error) {
      showNotification(error.response?.data?.message || 'Error deleting warehouse', 'error');
    }
  };

  const showNotification = (message, severity = 'success') => {
    setNotification({ open: true, message, severity });
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Warehouse Management
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Add New Warehouse
            </Typography>
            <form onSubmit={handleSubmit}>
              <TextField
                fullWidth
                label="Warehouse Name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                margin="normal"
                required
              />
              <TextField
                fullWidth
                label="Location"
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                margin="normal"
                required
              />
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                sx={{ mt: 2 }}
              >
                {editingId ? 'Update Warehouse' : 'Add Warehouse'}
              </Button>
            </form>
          </Paper>
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Warehouses
            </Typography>
            <List>
              {warehouses.map((warehouse) => (
                <ListItem key={warehouse.id} divider>
                  <ListItemText
                    primary={warehouse.name}
                    secondary={`Location: ${warehouse.location}`}
                  />
                  <ListItemSecondaryAction>
                    <IconButton
                      edge="end"
                      aria-label="edit"
                      onClick={() => handleEdit(warehouse)}
                      sx={{ mr: 1 }}
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      edge="end"
                      aria-label="delete"
                      onClick={() => handleDelete(warehouse.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
        <DialogTitle>Edit Warehouse</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Warehouse Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Location"
            value={formData.location}
            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
            margin="normal"
            required
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSubmit} color="primary">
            Update
          </Button>
        </DialogActions>
      </Dialog>

      <Notification
        open={notification.open}
        message={notification.message}
        severity={notification.severity}
        onClose={handleCloseNotification}
      />
    </Box>
  );
}

export default WarehousePage;
