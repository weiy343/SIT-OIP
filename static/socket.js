$(document).ready(function() {

    // Start connection
    var socket = io.connect("http://127.0.0.1:5000")

    // Starts the process
    $("#mainButton").on("click", function() {
        socket.send("Starting process");
    });

    // Receiving from server - entire washing process
    socket.on('message', function(data) {
        console.log("Received.");
        console.log(data);
        statusCountdown(data.time, data.status)
    });

    // Receiving from server - checking clealiness
    socket.on('check', function(data) {
        console.log("Received.");
        console.log(data);
        document.getElementById("status").innerHTML = data;
        document.getElementById("timer").innerHTML = " ";
    });
})

// Updates status and time left every second
function statusCountdown(totalSeconds, currentStatus) {

    var countdownTimer = setInterval(updateTime, 1000);
    
    document.getElementById("status").innerHTML = currentStatus;

    // Interval starts after 1 second
    totalSeconds = totalSeconds - 1

    function updateTime() {
        
        totalSeconds--

        if(totalSeconds == 0) {
            clearInterval(countdownTimer);
            document.getElementById("timer").innerHTML = "Completed";
        }
        else {
            minutes = (totalSeconds/60) | 0;
            seconds = totalSeconds % 60;
            document.getElementById("timer").innerHTML = "Estimated time: " + timeFormat(totalSeconds);
        }
    }
}

// Adds a prefix 0 if less than 10
function timeToString(time) {
    if (time < 10) {
        return `0${time}`
    }
    return `${time}`
}

// Format to mm:ss
function timeFormat(totalSeconds) {
    var minutes = (totalSeconds/60) | 0;
    var seconds = totalSeconds % 60;

    if (minutes < 10) {
        minutes = `0${minutes}`
    }
    if (seconds < 10) {
        seconds = `0${seconds}`
    }
    return `${minutes}:${seconds}`
}