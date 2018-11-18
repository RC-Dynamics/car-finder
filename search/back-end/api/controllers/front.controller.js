
var search_car = (req, res) => {
    console.log(req.query);
    // TODO: Set response to send to front
    res.status(200).json([{
        title : "BMW SERIES 3 2014 AUTOMATIC RED",
        transmission: "Manual",
        colour: "Red",
        price: "U$ 20.000",
        milage: "40000 miles",
        link: "https://www.kijiji.ca/"
    }, {
        title : "TOYOTA COROLLA",
        transmission: "Automatic",
        colour: "Black",
        price: "U$ 4.500",
        milage: "80000 miles",
        link: "https://shift.com/"
    }]);
}


module.exports = {
    search_car
}