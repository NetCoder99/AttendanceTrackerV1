$(document).ready(function() {
    console.log("Students Badge ready");
})

// ------------------------------------------------------------------
$('#btnCreateStudentBadge').off().on('click', function() {
    console.log("btnCreateStudentBadge was invoked");
    const badgeNumber = $('#hdnBadgeNumber').val();
    console.log(`btnCreateStudentBadge - badgeNumber: ${badgeNumber}`);
    const dataToSend = {'badgeNumber':badgeNumber};
    $.ajax({
      url: '/create_badge_api',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(dataToSend),
      dataType: 'text',
      success: function(response) {
        processCreateBadgeResponse(response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
})

function processCreateBadgeResponse(response) {
    console.log("processCreateBadgeResponse was invoked");
    response_json = JSON.parse(response);
    divStudentMessages = $('#divStudentMessages')
    if (response_json.status.toLowerCase() == 'ok'.toLowerCase()) {
        divStudentMessages.attr('class', 'fw-bold text-success');
        divStudentMessages.text(response_json.message)
    }
    else {
        divStudentMessages.attr('class', 'fw-bold text-danger');
        divStudentMessages.text('Error: ' + response_json.message)
    }
    setTimeout(() => {
        $('#divStudentMessages').html("Awaiting input ...");
        $('#divStudentMessages').removeClass('text-danger');
        $('#divStudentMessages').addClass('text-success');
    }, 5000);
}

// ------------------------------------------------------------------
$('#btnCreateStudentBadgeBattoDo').off().on('click', function() {
    console.log("btnCreateStudentBadgeBattoDo was invoked");
    const badgeNumber = $('#hdnBadgeNumber').val();
    console.log(`btnCreateStudentBadge - badgeNumber: ${badgeNumber}`);
    const dataToSend = {'badgeNumber':badgeNumber};
    $.ajax({
      url: '/create_batto_do_badge_api',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(dataToSend),
      dataType: 'text',
      success: function(response) {
        processCreateBattaDoBadgeResponse(response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });

})

function processCreateBattaDoBadgeResponse() {
    console.log("processCreateBattaDoBadgeResponse was invoked");

}