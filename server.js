const http = require('http');
const fs = require('fs');
const path = require('path');

const root = __dirname;
const port = 8000;

const contentTypes = {
  '.html': 'text/html; charset=utf-8',
  '.md': 'text/markdown; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8'
};

http
  .createServer((req, res) => {
    const urlPath = (req.url === '/' ? '/index.html' : req.url).split('?')[0];
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
  })
  .listen(port, '127.0.0.1', () => {
    console.log(`Server running at http://127.0.0.1:${port}`);
  });
