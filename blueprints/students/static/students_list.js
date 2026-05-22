$(document).ready(function() {
    console.log("Student List Document ready");
//    var studentListTable = $('#studentListTable').DataTable({
//        dom: '<"toolbar">frtip',
//        columnDefs: [{
//                targets: '_all', // Target all columns
//                className: 'dt-left' // Apply left alignment
//        }],
//        initComplete: function () {
//            $('div.toolbar').html('<button id="btnNewStudent" class="btn btn-success btn-new-student">New Student</button>');
//            $('#btnNewStudent').on('click', function() {
//                alert('Button clicked!');
//            });
//        }
//    });


    DataTable.type('num', 'className', 'dt-body-left');
    var studentListTable = $('#studentListTable').DataTable({
        dom: '<"toolbar">frtip',
        initComplete: function () {
            $('div.toolbar').html('<button id="btnNewStudent" class="btn btn-success btn-new-student">New Student</button>');
            $('#btnNewStudent').on('click', function() {
                window.location.replace("/student_create");
            });
        },
        "ajax": {
            "url": "student_list_api", // URL of your Python API
            "type": "GET",
            "dataSrc": ""   // Property in the JSON response
        },
        "columns": [
            {
                data: 'studentImageBase64',
                render: function(data, type, row, meta) {
                    // Combine prefix with base64 data from API
                    return '<img src="data:image/jpeg;base64,' + data + '" height="50" width="auto" />';
                }
            },
            { "data": "badgeNumber" },
            {
                data: null,
                render: function(data, type, row, meta) {
                    return row.firstName + ' ' + row.lastName;
                }
            },
            { "data": "currentRankName" },
        ]
    });

    $('#studentListTable tbody').on('click', 'tr', function() {
        console.log(`student row was clicked`);
        var rowData = studentListTable.row(this).data();
        $("#hdnBadgeNumber").val(rowData['badgeNumber']);
        processStudentEditClick(rowData['badgeNumber']);
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
    var table = $('#studentListTable').DataTable();
    table.ajax.reload();
}