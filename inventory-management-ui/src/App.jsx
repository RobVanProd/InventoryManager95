import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate, useNavigate } from 'react-router-dom';
import { Container, AppBar, Toolbar, Typography, Button, Box } from '@mui/material';

import HomePage from './pages/HomePage.jsx';
import AddPage from './pages/AddPage.jsx';
import ViewPage from './pages/ViewPage.jsx';
import LoginPage from './pages/LoginPage.jsx';
import WarehousePage from './pages/WarehousePage.jsx';
import DashboardPage from './pages/DashboardPage.jsx';
import { authService } from './services/auth';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = authService.isAuthenticated();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(authService.isAuthenticated());

  useEffect(() => {
    const checkAuth = () => {
      const token = authService.getToken();
      setIsAuthenticated(!!token);
    };

    checkAuth();
    // Set up an interval to check authentication status
    const interval = setInterval(checkAuth, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleLogout = () => {
    authService.logout();
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Inventory Manager 95
            </Typography>
            {isAuthenticated ? (
              <>
                <Button color="inherit" component={Link} to="/">Home</Button>
                <Button color="inherit" component={Link} to="/warehouses">Warehouses</Button>
                <Button color="inherit" component={Link} to="/add">Add Item</Button>
                <Button color="inherit" component={Link} to="/view">View Items</Button>
                <Button color="inherit" component={Link} to="/dashboard">Dashboard</Button>
                <Button color="inherit" onClick={handleLogout}>Logout</Button>
              </>
            ) : (
              <Button color="inherit" component={Link} to="/login">Login</Button>
            )}
          </Toolbar>
        </AppBar>

        <Container sx={{ mt: 3 }}>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
            <Route path="/warehouses" element={<ProtectedRoute><WarehousePage /></ProtectedRoute>} />
            <Route path="/add" element={<ProtectedRoute><AddPage /></ProtectedRoute>} />
            <Route path="/view" element={<ProtectedRoute><ViewPage /></ProtectedRoute>} />
            <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          </Routes>
        </Container>
      </Box>
    </Router>
  );
}

export default App;
