const front = require('../controllers/front.controller');

module.exports = (app) => {
    app.route('/search').get(front.search_car);
}