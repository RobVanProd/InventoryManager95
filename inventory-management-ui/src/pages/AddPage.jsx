import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Typography, TextField, Button, Box, MenuItem, Grid, Paper, Alert } from '@mui/material';
import { useFormik } from 'formik';
import { inventoryItemSchema } from '../validations/schemas';
import { inventoryApi } from '../services/api';
import Notification from '../components/Notification';

function AddPage() {
  const navigate = useNavigate();
  const [warehouses, setWarehouses] = useState([]);
  const [subWarehouses, setSubWarehouses] = useState([]);
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'success' });
  const [error, setError] = useState('');

  const showNotification = (message, severity = 'success') => {
    setNotification({ open: true, message, severity });
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  const formik = useFormik({
    initialValues: {
      name: '',
      quantity: '',
      description: '',
      price: '',
      warehouse: '',
      subwarehouse: '',
    },
    validationSchema: inventoryItemSchema,
    onSubmit: async (values, { setSubmitting, resetForm }) => {
      try {
        setError('');
        const formattedValues = {
          ...values,
          quantity: parseInt(values.quantity),
          price: values.price ? parseFloat(values.price) : null,
          warehouse: values.warehouse ? parseInt(values.warehouse) : null,
          subwarehouse: values.subwarehouse ? parseInt(values.subwarehouse) : null,
        };
        
        const response = await inventoryApi.createItem(formattedValues);
        showNotification(response.data.message || 'Item added successfully');
        resetForm();
        navigate('/view');
      } catch (error) {
        console.error('Error adding item:', error);
        setError(error.response?.data?.message || 'Error adding item. Please try again.');
      } finally {
        setSubmitting(false);
      }
    },
  });

  useEffect(() => {
    const fetchWarehouses = async () => {
      try {
        const response = await inventoryApi.getWarehouses();
        setWarehouses(response.data);
      } catch (error) {
        console.error('Error fetching warehouses:', error);
        setError('Error fetching warehouses. Please try again.');
      }
    };

    fetchWarehouses();
  }, []);

  useEffect(() => {
    const fetchSubWarehouses = async () => {
      if (formik.values.warehouse) {
        try {
          const response = await inventoryApi.getSubWarehouses();
          const filteredSubWarehouses = response.data.filter(
            sw => sw.warehouse === parseInt(formik.values.warehouse)
          );
          setSubWarehouses(filteredSubWarehouses);
        } catch (error) {
          console.error('Error fetching sub-warehouses:', error);
          setError('Error fetching sub-warehouses. Please try again.');
        }
      } else {
        setSubWarehouses([]);
      }
    };

    fetchSubWarehouses();
  }, [formik.values.warehouse]);

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 800, mx: 'auto', mt: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Add New Item
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <form onSubmit={formik.handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              id="name"
              name="name"
              label="Item Name"
              value={formik.values.name}
              onChange={formik.handleChange}
              error={formik.touched.name && Boolean(formik.errors.name)}
              helperText={formik.touched.name && formik.errors.name}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              id="quantity"
              name="quantity"
              label="Quantity"
              type="number"
              value={formik.values.quantity}
              onChange={formik.handleChange}
              error={formik.touched.quantity && Boolean(formik.errors.quantity)}
              helperText={formik.touched.quantity && formik.errors.quantity}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              id="price"
              name="price"
              label="Price"
              type="number"
              value={formik.values.price}
              onChange={formik.handleChange}
              error={formik.touched.price && Boolean(formik.errors.price)}
              helperText={formik.touched.price && formik.errors.price}
            />
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              id="warehouse"
              name="warehouse"
              select
              label="Warehouse"
              value={formik.values.warehouse}
              onChange={formik.handleChange}
              error={formik.touched.warehouse && Boolean(formik.errors.warehouse)}
              helperText={formik.touched.warehouse && formik.errors.warehouse}
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              {warehouses.map((warehouse) => (
                <MenuItem key={warehouse.id} value={warehouse.id}>
                  {warehouse.name} - {warehouse.location}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              id="subwarehouse"
              name="subwarehouse"
              select
              label="Sub-Warehouse"
              value={formik.values.subwarehouse}
              onChange={formik.handleChange}
              error={formik.touched.subwarehouse && Boolean(formik.errors.subwarehouse)}
              helperText={
                (formik.touched.subwarehouse && formik.errors.subwarehouse) ||
                (!formik.values.warehouse && 'Please select a warehouse first')
              }
              disabled={!formik.values.warehouse}
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              {subWarehouses
                .filter(sw => sw.warehouse === parseInt(formik.values.warehouse))
                .map((subwarehouse) => (
                  <MenuItem key={subwarehouse.id} value={subwarehouse.id}>
                    {subwarehouse.name}
                  </MenuItem>
                ))
              }
            </TextField>
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              id="description"
              name="description"
              label="Description"
              multiline
              rows={4}
              value={formik.values.description}
              onChange={formik.handleChange}
              error={formik.touched.description && Boolean(formik.errors.description)}
              helperText={formik.touched.description && formik.errors.description}
            />
          </Grid>

          <Grid item xs={12}>
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
              <Button
                type="button"
                variant="outlined"
                onClick={() => navigate('/view')}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                variant="contained"
                disabled={formik.isSubmitting}
              >
                Add Item
              </Button>
            </Box>
          </Grid>
        </Grid>
      </form>

      <Notification
        open={notification.open}
        message={notification.message}
        severity={notification.severity}
        onClose={handleCloseNotification}
      />
    </Paper>
  );
}

export default AddPage;
