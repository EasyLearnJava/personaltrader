const express = require('express');
const path = require('path');
const { spawn } = require('child_process');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = process.env.PORT || 3000;
const PYTHON_API_PORT = 5000;

// Proxy API requests to Python Flask server
app.use('/api', createProxyMiddleware({
  target: `http://localhost:${PYTHON_API_PORT}`,
  changeOrigin: true,
  onError: (err, req, res) => {
    console.error('Proxy error:', err);
    res.status(500).json({ error: 'Backend API unavailable' });
  }
}));

// Serve static files from the frontend/dist directory
app.use(express.static(path.join(__dirname, 'frontend', 'dist')));

// All other routes serve the React app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend', 'dist', 'index.html'));
});

// Start the Express server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Frontend server running on port ${PORT}`);
  console.log(`🌐 Access at: http://localhost:${PORT}`);
});

// Start the Python backend in a separate process
console.log('🐍 Starting Python backend...');
const pythonProcess = spawn('python', ['backend/main.py'], {
  stdio: 'inherit',
  env: process.env
});

pythonProcess.on('error', (error) => {
  console.error('❌ Failed to start Python backend:', error);
});

pythonProcess.on('exit', (code) => {
  console.log(`🐍 Python backend exited with code ${code}`);
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 SIGTERM received, shutting down gracefully...');
  pythonProcess.kill('SIGTERM');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('🛑 SIGINT received, shutting down gracefully...');
  pythonProcess.kill('SIGINT');
  process.exit(0);
});

