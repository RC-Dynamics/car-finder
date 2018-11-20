var fs = require('fs');

var search_car = (req, res) => {
    console.log(req.query);
    // TODO: Set response to send to front
    // search, transmission, colour, price, milage
    
    var index = JSON.parse(fs.readFileSync('./index.json', 'utf8'));
    var sites = JSON.parse(fs.readFileSync('./sitepool.json', 'utf8'));
    var extract = JSON.parse(fs.readFileSync('./extract.json', 'utf8'));
    
    var query_words = req.query.search.toLowerCase().split(" ");
    var query = {};
    var max_query = 0;
    var document = {};
    query_words.forEach(element => {
        var query_freq = 0;
        query[element] = {};
        if (index.hasOwnProperty(element)){
            index[element].forEach(element2 => {
                query_freq += element2["freq"];
                if (!document.hasOwnProperty(element2["doc"]))
                    document[element2["doc"]] = 0;
                document[element2["doc"]] += element2["freq"];
            });
        }
        query[element]["freq"] = query_freq;
        if(query_freq > max_query){
            max_query = query_freq;
        }
    });
    Object.keys(query).forEach(element => {
        if (index.hasOwnProperty(element)) {
            query[element]["tfidf"] = (0.5 + (0.5 * query[element]["freq"]) / max_query) * Math.log2(Object.keys(sites).length / index[element].length)
        } else
            query[element]["tfidf"] = 0;
    });

    var matrix = {}; // term x doc
    Object.keys(index).forEach(element => {
        matrix[element] = {};
        index[element].forEach(element2 => {
            matrix[element][element2["doc"]] = element2["freq"] * Math.log2(Object.keys(sites).length / index[element].length); 
            // console.log(`${matrix[element][element2["doc"]]} - ${element2["freq"]} * ${Object.keys(sites).length} / ${index[element].length}`);
        });
    });
    // console.log(matrix);
    // console.log(query);
    var scores = {};
    Object.keys(matrix).forEach(element => {
        Object.keys(matrix[element]).forEach(element2 => {
            if (!scores.hasOwnProperty(element2))
                scores[element2] = 0;
            if (query.hasOwnProperty(element)){
                if (query[element].hasOwnProperty("tfidf"))
                    scores[element2] += matrix[element][element2] * query[element]["tfidf"];
            }
            
        });
    });

    var rank_cos = Object.keys(scores).map(function (key) {
        return [key, scores[key]];
    });

    rank_cos.sort(function (first, second) {
        return second[1] - first[1];
    });

    var rank_freq = Object.keys(document).map(function (key) {
        return [key, document[key]];
    });

    rank_freq.sort(function (first, second) {
        return second[1] - first[1];
    });
    // console.log(rank_cos)
    // console.log(rank_freq);


    // TODO Kenda Tau
    // TODO Spearman
    var answer = [];
    var max_search = 5;
    for(var i = 0; i < max_search; i++){
        if (req.query.transmission.toLowerCase() == extract[rank_cos[i][0]]["Transmission"].toLowerCase() || req.query.transmission.toLowerCase() == "none"){
            if (req.query.colour.toLowerCase() == extract[rank_cos[i][0]]["Exterior Color"].toLowerCase() || req.query.colour.toLowerCase() == "none") {
                // if (req.query.milage == extract[rank[i][0]]["Exterior Color"].toLowerCase()) {
                answer.push({
                    title: extract[rank_cos[i][0]]["Title"],
                    transmission: extract[rank_cos[i][0]]["Transmission"],
                    colour: extract[rank_cos[i][0]]["Exterior Color"],
                    price: extract[rank_cos[i][0]]["Price"],
                    milage: extract[rank_cos[i][0]]["Mileage"],
                    link: sites[rank_cos[i][0]]
                })
                continue;
                // }    
            }
        }
        // max_search++;
        
    }
    // console.log(answer)
    res.status(200).json(answer)


    // res.status(200).json([{
    //     title : "BMW SERIES 3 2014 AUTOMATIC RED",
    //     transmission: "Manual",
    //     colour: "Red",
    //     price: "U$ 20.000",
    //     milage: "40000 miles",
    //     link: "https://www.kijiji.ca/"
    // }, {
    //     title : "TOYOTA COROLLA",
    //     transmission: "Automatic",
    //     colour: "Black",
    //     price: "U$ 4.500",
    //     milage: "80000 miles",
    //     link: "https://shift.com/"
    // }]);
}


module.exports = {
    search_car
}