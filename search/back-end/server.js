const express = require('./api/config/express');

var app = express();

const port = 1337;
app.listen(port);
console.log('server running at http://localhost:' + port);