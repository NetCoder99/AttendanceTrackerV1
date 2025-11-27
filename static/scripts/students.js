$(document).ready(function() {
    console.log("Students Document ready");

    $('#studentBtnSearch').on('click', function() {
        console.log("studentBtnSearch was clicked");
        event.preventDefault();
        $.ajax({
            url: '/student_search', // The Flask route to call
            type: 'POST',
            contentType: 'application/json',
            dataType: "json",
            data: JSON.stringify(
                {
                  'searchFirstName'  : $('#searchFirstName').val(),
                  'searchLastName'   : $('#searchLastName').val(),
                  'searchBadgeNumber': $('#searchBadgeNumber').val()
                }
            ), // Optional: send data
            success: function(response) {
                processSearchResponse(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
})

// -------------------------------------------------------------------------------
function processSearchResponse(response) {
    console.log("processCheckinResponse was invoked.");
    student_card = $('#divStaticCard').find('#divStudentCard');
    let divStudentsList = $('#divStudentsList');
    divStudentsList.empty();
    $.each(response, function(index, value) {
        student_card.find('#studentBadgeNumber').html(value.badgeNumber);
        student_card.find('#studentStudentName').html(value.firstName + ' ' + value.lastName);
        student_card.find('#studentRankName').html(value.currentRankName);
        student_card.find('#studentImage').attr({
            "src": `data:image/${value.studentImageType};base64,${value.studentImageBase64}`
        });
        divStudentsList.append(student_card.clone(true));
        console.log("Index: " + index + ", Value: " + value.badgeNumber);
    });
}

