// Button fuction
$(function () {
    $('main').on('click', function (e) {
        console.log("send");
        e.preventDefault()
        $.getJSON('/start',
            function (data) {
                //do nothing
            });
        return false;
    });
});