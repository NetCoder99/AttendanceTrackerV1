function ShowDeleteStudentConfirmation() {
    const badgeNumber = $('#hdnBadgeNumber').val();
    console.log("*** ShowDeleteStudentConfirmation: Clicked ***");
//    divStudentMessages = $('#divStudentMessages');
//    divStudentMessages.removeClass('text-danger');
//    divStudentMessages.removeClass('text-success');
//    divStudentMessages.text("Deleting student record!");

    divStudentDeleteConfirmations = $('#divStudentDeleteConfirmations');
    divStudentDeleteConfirmations.removeClass('removed');

    divStudentConfirmation = $('#divStudentConfirmation');
    divStudentConfirmation.addClass('removed');

    setTimeout(() => {
        $('#divStudentMessages').html("Awaiting input ...");
        $('#divStudentMessages').removeClass('text-danger');
        $('#divStudentMessages').addClass('text-success');
    }, 3000);
}

function HideStudentDeletePanel() {
    console.log("*** HideStudentDeletePanel: Clicked ***");
    $('#divStudentDeleteConfirmations').addClass('removed');
    $('#divStudentConfirmation').removeClass('removed');
    setTimeout(() => {
        $('#divStudentMessages').html("Awaiting input ...");
        $('#divStudentMessages').removeClass('text-danger');
        $('#divStudentMessages').addClass('text-success');
    }, 5000);
}

function DeleteStudentRecordApi() {
    console.log("*** DeleteStudentRecordApi: Clicked ***");
    $("#btnClassConfirmDeleteNo").prop("disabled", true);
    $("#btnClassConfirmDeleteYes").prop("disabled", true);
    $("#lblConfirmClassDelete").text("Processing...");

    console.log($("#divStudentMessages").length);
    const badgeNumber = $('#hdnBadgeNumber').val();
    const payload = { hdnBadgeNumber: badgeNumber };
    try {
        $.ajax({
            url: '/student_delete_confirmation_api?' + $.param(payload),
            type: 'POST',
            success: function(response) {
                console.log('Success:', response);
                ProcessDeleteStudentResponse(response);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Status: " + textStatus); alert("Error: " + errorThrown);
            }
        });
    } catch (error) {
        console.error('Error:', error);
    }
    console.log("*** DeleteStudentRecordApi: Completed ***");
}

function ProcessDeleteStudentResponse(response) {
    if (response.status == 'ok') {
        $("#divStudentRecover").removeClass('removed');
        $("#divStudentDeleteConfirmations").addClass('removed');
//        $("#btnClassConfirmDeleteNo").addClass('removed');
//        $("#btnClassConfirmDeleteYes").addClass('removed');
//        $("#lblConfirmClassDelete").text(response.message);
    }
    else {
        $("#lblConfirmClassDelete").text(response.message);
    }

}