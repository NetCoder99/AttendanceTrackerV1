$(document).ready(function() {
    console.log("Student List Document ready");
    var studentListTable = $('#studentListTable').DataTable({
        dom: 'Bfrtip',
        buttons: [{
                text: 'New Student',
                className: 'btn btn-success',
                action: function ( e, dt, node, config ) {
                    alert('Custom button activated!');
                }
        }],
        columnDefs: [{
                targets: '_all', // Target all columns
                className: 'dt-left' // Apply left alignment
        }]
    });

    $('#studentListTable tbody').on('click', 'tr', function() {
        console.log(`student row was clicked`);
        var rowData = studentListTable.row(this).data();
        $("#hdnBadgeNumber").val(rowData[1]);
        processStudentEditClick(rowData[1]);
    });
})

// -------------------------------------------------------------------------------
function processStudentEditClick(badgeNumber) {
    console.log(`processStudentEditClick was invoked: ${badgeNumber}`);
    const badgeNbr = $('#studentBadgeNumber').html();
    var triggerEl = document.querySelector('#tabStudentDetails');
    var tab = bootstrap.Tab.getOrCreateInstance(triggerEl);
    tab.show(); // Show the tab and its content
}

function InitializeStudentsList() {
    console.log(`InitializeStudentsList`);
    fetch('/student_list_api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response       => response.json())
    .then(studentRecords => DisplayStudentRecords(studentRecords))
    .catch(error         => console.error('Error:', error));
}

function DisplayStudentRecords(studentRecords) {
    console.log(`DisplayStudentRecords was invoked: ${studentRecords.length}`);

}