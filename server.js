//
// ==================== AI / IMPLEMENTATION LOG ====================
//
// This server file was initially created by Alex using AI generated code.
//
// INITIAL AI PROMPT (ChatGPT):
// "Create a Node.js HTTP server that serves static files and includes an API proxy
//  endpoint (/api/mushroom/identify) which reads a .env file for API credentials,
//  forwards image data to a mushroom identification API, and returns the response."
//
// Ben Wingfield added onto this file with the Kindwise API for machine learning mushroom identification
// AI PROMPT (ChatGPT):
// "https://github.com/flowerchecker/mushroom-id-examples
//  Could we integrate this API into the current code [index.html, server.js] please?"
//
// The generated server includes:
// - Basic static file serving using Node's http/fs/path modules
// - Custom .env loader without external dependencies
// - JSON request parsing utility
// - API proxy endpoint for mushroom identification requests to Kindwise and processing of what is returned
//
// =================================================================

const http = require('http');
const fs = require('fs');
const path = require('path');

const root = __dirname;
const port = Number(process.env.PORT || 8000);
const DEFAULT_API_BASE_URL = 'https://mushroom.kindwise.com/api/v1/';
const DEFAULT_DETAILS = [
  'common_names',
  'url',
  'taxonomy',
  'rank',
  'characteristic',
  'edibility',
  'psychoactive',
  'gbif_id'
];

function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) return;
  const lines = fs.readFileSync(filePath, 'utf8').split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eq = trimmed.indexOf('=');
    if (eq === -1) continue;
    const key = trimmed.slice(0, eq).trim();
    let value = trimmed.slice(eq + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (!process.env[key]) process.env[key] = value;
  }
}

loadEnvFile(path.join(root, '.env'));

const contentTypes = {
  '.html': 'text/html; charset=utf-8',
  '.md': 'text/markdown; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8'
};

function sendJson(res, statusCode, payload) {
  res.writeHead(statusCode, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(payload));
}

function stripDataUrl(dataUrl) {
  if (typeof dataUrl !== 'string') return '';
  const comma = dataUrl.indexOf(',');
  return comma >= 0 ? dataUrl.slice(comma + 1) : dataUrl;
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', (chunk) => chunks.push(chunk));
    req.on('end', () => {
      try {
        const raw = Buffer.concat(chunks).toString('utf8');
        resolve(raw ? JSON.parse(raw) : {});
      } catch (error) {
        reject(error);
      }
    });
    req.on('error', reject);
  });
}

async function proxyIdentification(req, res) {
  const baseUrl = process.env.MUSHROOM_API_BASE_URL || DEFAULT_API_BASE_URL;
  const apiKey = process.env.MUSHROOM_API_KEY;
  if (!apiKey) {
    sendJson(res, 500, { error: 'Missing MUSHROOM_API_KEY in .env' });
    return;
  }

  let payload;
  try {
    payload = await readBody(req);
  } catch {
    sendJson(res, 400, { error: 'Invalid JSON body' });
    return;
  }

  const images = Array.isArray(payload.images) ? payload.images.map(stripDataUrl).filter(Boolean) : [];
  if (images.length === 0) {
    sendJson(res, 400, { error: 'At least one image is required' });
    return;
  }

  const endpoint = new URL('identification', baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`);
  endpoint.searchParams.set('details', DEFAULT_DETAILS.join(','));

  const upstreamPayload = {
    images,
    similar_images: payload.similar_images !== false,
    datetime: payload.datetime || undefined,
    latitude: typeof payload.latitude === 'number' ? payload.latitude : undefined,
    longitude: typeof payload.longitude === 'number' ? payload.longitude : undefined
  };

  const upstream = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Api-Key': apiKey
    },
    body: JSON.stringify(upstreamPayload)
  });

  const text = await upstream.text();
  if (!upstream.ok) {
    sendJson(res, 502, { error: 'Kindwise mushroom.id request failed', status: upstream.status, body: text });
    return;
  }

  res.writeHead(upstream.status, {
    'Content-Type': upstream.headers.get('content-type') || 'application/json; charset=utf-8'
  });
  res.end(text);
}

http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || '127.0.0.1'}`);
  if (req.method === 'POST' && url.pathname === '/api/mushroom/identify') {
    proxyIdentification(req, res).catch((error) => sendJson(res, 500, { error: error.message || 'Unexpected server error' }));
    return;
  }

  const urlPath = url.pathname === '/' ? '/index.html' : url.pathname;
  const filePath = path.join(root, urlPath);
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('not found');
      return;
    }
    const type = contentTypes[path.extname(filePath).toLowerCase()] || 'text/plain; charset=utf-8';
    res.writeHead(200, { 'Content-Type': type });
    res.end(data);
  });
}).listen(port, '127.0.0.1', () => {
  console.log(`Server running at http://127.0.0.1:${port}`);
});