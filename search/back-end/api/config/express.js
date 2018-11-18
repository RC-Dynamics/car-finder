const express = require('express');

module.exports = () => {
    var app = express();
    
    app.use((req, res, next) => {
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
        next();
    });

    require('../routes/front.routes')(app);

    return app;
}