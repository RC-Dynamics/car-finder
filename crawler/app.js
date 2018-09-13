const request = require('request');

const sites = require('./res/sites.js');

sites.forEach(site => {
    request({
        url: site + "robots.txt"
    }, (err, res, body) => {
        console.log(`${site} - ${res.statusCode}`);
        if (res.statusCode == 200){
            console.log(body);
        }
    });
    
});
