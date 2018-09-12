const request = require('request');

request({
    url: "https://www.kijiji.ca/"
}, (err, res, body) => {
    console.log(body);
});