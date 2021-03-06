$(document).ready(function() {

    // Start connection
    var socket = io.connect("http://127.0.0.1:5000")

    // Starts the process
    $("#mainButton").on("click", function() {
        document.getElementById("mainButton").classList.add("disabled");
        socket.send();
    });

    // Receiving from server - entire washing process
    socket.on('message', function(data) {
        console.log("Received.");
        console.log(data);
        statusCountdown(data.time, data.status)
    });

    // Receiving from server - checking cleanliness
    socket.on('check', function(data) {
        console.log("Received.");
        console.log(data);
        document.getElementById("status").innerHTML = data;
        document.getElementById("timer").innerHTML = " ";
    });

    // Receiving from server - checking heat
    socket.on('heating', function(data) {
        console.log("Received.");
        console.log(data);
        document.getElementById("status").innerHTML = data.status;
        document.getElementById("timer").innerHTML = "Current temperature: " + data.temp;
    });

    // Receiving from server - checking cover if closed
    socket.on('coverWarning', function(data) {
        console.log("Received.");
        console.log(data);
        document.getElementById("mainButton").classList.remove("disabled");
        document.getElementById("status").innerHTML = data;
        document.getElementById("timer").innerHTML = " ";
    });

    // Receiving from server - reenable button
    socket.on('complete', function() {
        document.getElementById("mainButton").classList.remove("disabled");
        document.getElementById("status").innerHTML = "All syringes are cleaned.";
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