// Button fuction
$(function () {
    $('mainButton').on('click', function (e) {
        console.log("send");
        e.preventDefault()
        $.getJSON('/start',
            function (data) {
                //do nothing
            });
        return false;
    });
});


// Starts countdown when the button is clicked.
document.getElementById("mainButton").addEventListener("click", function() {
    statusCountdown(200, "hello")
});

// Updates status and time left every second
function statusCountdown(seconds, currentStatus) {

    document.getElementById("status").innerHTML = currentStatus;

    // Convert to minutes and seconds
    var minutes = (seconds/60) | 0;
    var seconds = seconds % 60;

    var countdownTimer = setInterval(updateTime, 100);
    
    // Can be changed to convert everytime instead for readability
    function updateTime() {

        // Completion
        if (seconds + minutes == 0) {
            clearInterval(countdownTimer);
            document.getElementById("timer").innerHTML = `completed`;
            return;
        }

        // Update time text
        document.getElementById("timer").innerHTML = `${minutes}:${seconds}`;
        if (seconds == 0) {
            seconds = 59;
            minutes--;
        }
        else {
            seconds--;
        }
    }
}