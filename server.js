import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import https from 'https';
import http from 'http';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static assets from dist
app.use(express.static(path.join(__dirname, 'dist')));

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

// Single Page Application (SPA) fallback
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);

  // Determine external URL for self-ping
  const targetUrl = process.env.RENDER_EXTERNAL_URL || 'https://yashwanthgowda-portfolio.onrender.com';
  console.log(`Keep-alive self-ping target: ${targetUrl}`);

  const ping = () => {
    try {
      const client = targetUrl.startsWith('https') ? https : http;
      client.get(targetUrl, (res) => {
        console.log(`[Keep-Alive] Pinged ${targetUrl} (Status: ${res.statusCode}) at ${new Date().toISOString()}`);
      }).on('error', (err) => {
        console.warn(`[Keep-Alive] Ping error: ${err.message}`);
      });
    } catch (err) {
      console.warn(`[Keep-Alive] Unexpected error: ${err.message}`);
    }
  };

  // Ping every 10 minutes (600,000 ms) to prevent Render free tier inactivity spin-down
  const INTERVAL_MS = 10 * 60 * 1000;
  setInterval(ping, INTERVAL_MS);
});
