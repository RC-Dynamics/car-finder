const express = require('express');

module.exports = () => {
    var app = express();
    // app.use(express.bodyParser());

    require('../routes/front.routes')(app);

    return app;
}