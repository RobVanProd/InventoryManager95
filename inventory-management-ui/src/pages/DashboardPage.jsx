import React, { useState, useEffect } from 'react';
import {
  Typography,
  Grid,
  Paper,
  Box,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Inventory as InventoryIcon,
  Warehouse as WarehouseIcon,
  Warning as WarningIcon,
  Timeline as TimelineIcon,
  AttachMoney as MoneyIcon,
} from '@mui/icons-material';
import { inventoryApi } from '../services/api';

function DashboardCard({ title, value, icon, color }) {
  return (
    <Card elevation={3}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          {icon}
          <Typography variant="h6" component="div" sx={{ ml: 1 }}>
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" component="div" color={color}>
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
}

function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await inventoryApi.getDashboardStats();
        console.log('Dashboard stats response:', response.data);
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
        setError('Failed to load dashboard statistics. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ mt: 2 }}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Inventory Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Summary Cards */}
        <Grid item xs={12} sm={6} md={4}>
          <DashboardCard
            title="Total Items"
            value={stats?.total_items ?? 0}
            icon={<InventoryIcon color="primary" />}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <DashboardCard
            title="Total Warehouses"
            value={stats?.total_warehouses ?? 0}
            icon={<WarehouseIcon color="secondary" />}
            color="secondary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <DashboardCard
            title="Low Stock Items"
            value={stats?.low_stock_items ?? 0}
            icon={<WarningIcon color="error" />}
            color="error"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <DashboardCard
            title="Recent Items (7 days)"
            value={stats?.recent_items ?? 0}
            icon={<TimelineIcon color="info" />}
            color="info"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <DashboardCard
            title="Total Value"
            value={stats?.total_value != null ? `$${Number(stats?.total_value).toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })}` : '$0.00'}
            icon={<MoneyIcon color="success" />}
            color="success"
          />
        </Grid>

        {/* Warehouse Distribution */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Items by Warehouse
            </Typography>
            <List>
              {stats?.items_by_warehouse?.length > 0 ? (
                stats.items_by_warehouse.map((warehouse, index) => (
                  <React.Fragment key={warehouse?.warehouse__name || 'unassigned'}>
                    {index > 0 && <Divider />}
                    <ListItem>
                      <ListItemText
                        primary={warehouse?.warehouse__name || 'Unassigned'}
                        secondary={`${warehouse?.count ?? 0} items`}
                      />
                    </ListItem>
                  </React.Fragment>
                ))
              ) : (
                <ListItem>
                  <ListItemText primary="No warehouse data available" />
                </ListItem>
              )}
            </List>
          </Paper>
        </Grid>

        {/* Additional Stats */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Quick Stats
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Average Items per Warehouse"
                  secondary={stats?.total_warehouses ? (stats?.total_items / stats?.total_warehouses).toFixed(1) : '0'}
                />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText
                  primary="Sub-Warehouses"
                  secondary={`${stats?.total_subwarehouses ?? 0} total`}
                />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText
                  primary="Low Stock Alert"
                  secondary={`${stats?.low_stock_items ?? 0} items below 10 units`}
                />
              </ListItem>
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default DashboardPage;
