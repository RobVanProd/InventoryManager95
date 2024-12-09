require('dotenv').config();
const express = require('express');
const path = require('path');
const cors = require('cors');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet());
app.use(cors({
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    credentials: true
}));

// Performance middleware
app.use(compression());
app.use(express.json());
app.use(morgan('combined'));

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'inventory-management-ui/build')));

// API routes will go here
app.get('/api/health', (req, res) => {
    res.json({ status: 'healthy' });
});

// The "catchall" handler: for any request that doesn't
// match one above, send back React's index.html file.
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'inventory-management-ui/build/index.html'));
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
