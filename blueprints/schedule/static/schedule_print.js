// ------------------------------------------------------------------
$('#btnPrintSchedulePDF').off().on('click', function() {
    console.log("btnPrintSchedulePDF was invoked");
    $.ajax({
      url: '/print_schedule_api',
      type: 'POST',
      contentType: 'application/json',
      data: null,
      dataType: 'text',
      success: function(response) {
        processPrintScheduleResponse(response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
})

function processPrintScheduleResponse(response) {
    console.log("processPrintScheduleResponse was called");
    response_json = JSON.parse(response)
    $("#divScheduleMessage").removeClass()
    $("#divScheduleMessage").addClass('fw-bold');
    if (response_json.status == 'error') {
        $("#divScheduleMessage").html(`Error: ${response_json.message}`);
        $("#divScheduleMessage").addClass('text-danger');
    } else {
        $("#divScheduleMessage").html(`${response_json.message}`);
        $("#divScheduleMessage").addClass('text-success');
    }
    setTimeout(() => {
        $("#divScheduleMessage").html("&nbsp");
        $('#divStudentMessages').removeClass();
    }, 4000);
}
