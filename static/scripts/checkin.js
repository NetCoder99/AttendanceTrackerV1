$(document).ready(function() {
    console.log("Document ready");
    $('#currentDateTime').text(getDisplayDate());
    $('#badgeNumber').focus();
    let myInterval = setInterval(function() {
        $('#currentDateTime').text(getDisplayDate());
        $('#badgeNumber').focus();
    }, 1000);

    $('#checkinTimer5').addClass("hidden");
    $('#checkinTimer4').addClass("hidden");
    $('#checkinTimer3').addClass("hidden");
    $('#checkinTimer2').addClass("hidden");
    $('#checkinTimer1').addClass("hidden");
    $('#checkinMessage2').addClass("removed");
    $('#checkinMessage3').addClass("removed");

    $('#badgeNumber').keydown(function(event) {
        console.log("badgeNumber keydown");
        if (event.which === 13) {
          event.preventDefault();
          processCheckinAction(event);
          console.log("Enter key pressed, default action prevented.");
        }
    });

})

// -------------------------------------------------------------------------------
function getDisplayDate(inpDate = new Date()) {
    const date = inpDate.toLocaleDateString();
    const time = inpDate.toLocaleTimeString();
    const day  = inpDate.toLocaleDateString('en-us',{ weekday: 'long' });
    return `${day} ${date} ${time}`;
}

// -------------------------------------------------------------------------------
function processCheckinAction(event) {
    $('#badgeNumber').prop('disabled', true);
    $('#checkinTimer5').removeClass("hidden");
    $('#checkinTimer4').removeClass("hidden");
    $('#checkinTimer3').removeClass("hidden");
    $('#checkinTimer2').removeClass("hidden");
    $('#checkinTimer1').removeClass("hidden");

    const badgeNumber = $('#badgeNumber').val();
    console.log(`badgeNumber: ${badgeNumber}`);
    $.post("/checkin", {"badgeNumber": badgeNumber}, function(response) {
        processCheckinResponse(response);
    });
}

// -------------------------------------------------------------------------------
function processCheckinResponse(response) {
    $('#badgeNumber').val(null)
    $('#checkinMessage1').html(response.message)
    $('#checkinMessage1').removeClass("text-success");
    $('#checkinMessage1').removeClass("text-danger");
    if (response.status == 'error') {
        $('#checkinMessage1').addClass("text-danger");
        $('#checkinMessage2').addClass("removed");
        $('#checkinMessage3').addClass("removed");
    }
    else {
        let className = response.classData.classDisplayTitle;
        $('#checkinMessage1').html(className)
        $('#checkinMessage1').addClass("text-success");
        $('#checkinMessage2').removeClass("removed");
        $('#checkinMessage3').removeClass("removed");
    }
    let count = 5;
    const intervalID = setInterval(() => {
      console.log(`Tick: ${count}`);
      $('#checkinTimer'+count).addClass("hidden");
      count--;
      checkinTimer5
    }, 1000);

    setTimeout(() => {
      clearInterval(intervalID);
      console.log("Interval stopped.");
    }, 6000);

    setTimeout(() => {
      resetCheckinScreen();
    }, 6000);
}

// -------------------------------------------------------------------------------
function resetCheckinScreen(response) {
    $('#badgeNumber').prop('disabled', false);
    $('#checkinMessage1').html("Waiting ...")
    $('#checkinMessage1').removeClass("text-success");
    $('#checkinMessage1').removeClass("text-danger");
    $('#checkinMessage2').addClass("removed");
    $('#checkinMessage3').addClass("removed");
}