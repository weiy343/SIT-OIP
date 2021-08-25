// Starts countdown when the button is clicked.
document.getElementById("mainButton").addEventListener("click", async function() {
    await fetchProcess("/pump");
    await fetchProcess("/wash");
    await fetchProcess("/drain");
    await fetchProcess("/dry");
    await fetchProcess("/sterilize");
});

// Fetch function to reduce copy paste
async function fetchProcess(url){
    const response = await fetch(`${url}`);
    const json = await response.json();
    await statusCountdown(json.time, json.status);
    return;
}

// Updates status and time left every second
function statusCountdown(totalSeconds, currentStatus) {

    return new Promise(function(resolve, reject) {

        // Convert to minutes and seconds to string
        var minutes = (totalSeconds/60) | 0;
        var seconds = totalSeconds % 60;
    
        var countdownTimer = setInterval(updateTime, 1000);
        
        document.getElementById("status").innerHTML = currentStatus;

        // Can be changed to convert everytime instead for readability
        function updateTime() {
    
            // Completion
            if (seconds + minutes == 0) {
                clearInterval(countdownTimer);
                document.getElementById("timer").innerHTML = "Completed";
                resolve();
                return;
            }
    
            // Update time text
            document.getElementById("timer").innerHTML = timeFormat(minutes, seconds);
            if (seconds == 0) {
                seconds = 59;
                minutes--;
            }
            else {
                seconds--;
            }
        }
    });
}

// Adds a prefix 0 if less than 10
function timeToString(time) {
    if (time < 10) {
        return `0${time}`
    }
    return `${time}`
}

// Format to mm:ss
function timeFormat(minutes, seconds) {
    if (minutes < 10) {
        minutes = `0${minutes}`
    }
    if (seconds < 10) {
        seconds = `0${seconds}`
    }
    return `${minutes}:${seconds}`
}