$(document).ready(function () {
    $("form").submit(function (e) {
        e.preventDefault();
        var form = $(this);
        
        $.ajax({
            url: "http://localhost:1337/search",
            data: form.serialize(),
            type: "GET",
            success: function (responseData) {
                // console.log(responseData);
                var result_div = $("#show-res-data");
                responseData.forEach(element => {
                    
                    result_div.append(`<div>
                    <a href="${element.link}"><h3>${element.title}</h3></a>
                    <p class="item-info lead">Price: ${element.price}</p>
                    <p class="item-info lead">Colour: ${element.colour}</p>
                    <p class="item-info lead">Milage: ${element.milage}</p>
                    <p class="item-info lead">Transmission: ${element.transmission}</p>
                    <\div>`);
                });
            },
            error: console.error
        });
    });
});