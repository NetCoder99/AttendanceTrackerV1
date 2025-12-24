$(document).ready(function() {
    console.log("Students Badge ready");
})

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

function processCreateBadgeResponse() {
    console.log("processCreateBadgeResponse was invoked");

}