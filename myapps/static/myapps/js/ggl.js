$(function () {
    $('.price').each(function () {
        let price = $(this).text()
        if (price <= 800) {
            $(this).css("background-color", "orange");
        } else if (price > 800 && price <= 1000) {
            $(this).css("background-color", "green");
        } else if (price > 1000 && price <= 1200) {
            $(this).css("background-color", "pink");
        } else if (price > 1200 && price <= 1500) {
            $(this).css("background-color", "yellow");
        } else if (price > 1500 && price <= 2000) {
            $(this).css("background-color", "blue");
        } else if (price > 2000) {
            $(this).css("background-color", "red");
        }
    })
})