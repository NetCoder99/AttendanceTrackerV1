$(document).ready(function() {
    console.log("Student List Document ready");
    var studentListTable = $('#studentListTable').DataTable({
        buttons: [
                {
                    text: 'Create new student',
                    className: 'dt-button',
                    action: function (e, dt, node, config) {
                        console.log("Create student clicked");
                    }
                }
        ],
        layout: {
            topStart: 'buttons'
        },
        columnDefs: [{
                targets: '_all', // Target all columns
                className: 'dt-left' // Apply left alignment
        }],
        initComplete: function () {
            var btns = $('.dt-button');
            btns.addClass('btn btn-success btn-sm float-end');
            btns.removeClass('btn-secondary');

        }
    });
    $('#studentListTable tbody').on('click', 'tr', function() {
        console.log(`student row was clicked`);
        var rowData = studentListTable.row(this).data();
        processStudentEditClick(rowData[1]);
    });

    $("#btnCreateStudent").on("click", function(event) {
        console.log("The create student was clicked!");
    });
})

$("classCreateStudent").click(function(event) {
    console.log("The create student was clicked!");
});

// -------------------------------------------------------------------------------
function processStudentEditClick(badgeNumber) {
    console.log(`processStudentEditClick was invoked: ${badgeNumber}`);
    const badgeNbr = $('#studentBadgeNumber').html();
    window.location.href = `/student_details?badgeNumber=${badgeNumber}`;
}

//// -------------------------------------------------------------------------------
//function processSearchClick() {
//    console.log("processSearchClick was invoked");
//    $.ajax({
//        url: '/student_search', // The Flask route to call
//        type: 'POST',
//        contentType: 'application/json',
//        dataType: "json",
//        data: JSON.stringify(
//            {
//              'searchFirstName'  : $('#searchFirstName').val(),
//              'searchLastName'   : $('#searchLastName').val(),
//              'searchBadgeNumber': $('#searchBadgeNumber').val()
//            }
//        ), // Optional: send data
//        success: function(response) {
//            processSearchResponse(response);
//        },
//        error: function(error) {
//            console.log(error);
//        }
//    });
//}
