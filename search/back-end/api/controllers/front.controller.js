
var search_car = (req, res) => {
    console.log(req.query);
    res.status(200).json({
        // TODO: Set response to send to front
        a : "abc"
    });
}


module.exports = {
    search_car
}