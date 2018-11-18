$(document).ready(function () {
    $("form").submit(function (e) {
        e.preventDefault();
        var form = $(this);
        
        $.ajax({
            url: "http://localhost:1337/search",
            data: form.serialize(),
            type: "GET",
            success: function (responseData) {
                // TODO: Display data from server
                console.log(responseData);
            },
            error: console.error
        });
    });
});