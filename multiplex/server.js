const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const crypto = require('crypto');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: '*', methods: ['GET', 'POST'] }
});

app.get('/token', (req, res) => {
  const secret = crypto.randomBytes(64).toString('hex');
  const socketId = crypto.createHash('md5').update(secret).digest('hex');
  res.json({ secret, socketId });
});

io.on('connection', (socket) => {
  socket.on('multiplex-statechanged', (data) => {
    if (!data.secret || !data.socketId) return;
    const valid = crypto.createHash('md5').update(data.secret).digest('hex') === data.socketId;
    if (!valid) return;
    socket.join(data.socketId);
    socket.broadcast.to(data.socketId).emit(data.socketId, data);
  });

  socket.on('multiplex-join', (data) => {
    if (data.socketId) socket.join(data.socketId);
  });
});

const port = process.env.PORT || 1948;
server.listen(port, () => console.log(`Multiplex server on port ${port}`));
