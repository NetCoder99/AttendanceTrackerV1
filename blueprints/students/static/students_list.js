$(document).ready(function() {
    console.log("Student List Document ready");
    DataTable.type('num', 'className', 'dt-body-left');
    var studentListTable = $('#studentListTable').DataTable({
        dom: '<"toolbar">frtip',
        initComplete: function () {
            $('div.toolbar').html('<button id="btnNewStudent" class="btn btn-success btn-new-student">New Student</button>');
            $('#btnNewStudent').on('click', function() {
                window.location.replace("/display_student_create");
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
            { "data": "currentStripeName" },
            { "data": "memberSinceDate",
                className: 'dt-left',
                render: function (data, type, row) {
                    if (!data) return '';
                    if (type === 'display') {
                        const date = new Date(data);
                        return date.toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: '2-digit',
                            day: '2-digit'
                        }); // Returns MM/DD/YYYY
                    }
                    return data;
                }
            },

        ]
    });

    $('#studentListTable tbody').on('click', 'tr', function() {
        console.log(`student row was clicked`);
        var rowData = studentListTable.row(this).data();
        $("#hdnBadgeNumber").val(rowData['badgeNumber']);
        processStudentEditClick(rowData['badgeNumber']);
    });

    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    studentListTable.ready(function () {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('search_term')) {
            const search_term = urlParams.get('search_term');
            console.log(`  search_term: ${search_term}`);
            const search_box = $('#dt-search-0') ;
            if (search_box) {
                search_box.val(search_term);
                console.log(`  search_box_val: ${search_box.val()}`);
            }
            search_box.focus();

            const e = $.Event('keydown');
            e.which = 13;
            e.keyCode = 13;
            search_box.trigger(e);

        }
    });
})

//window.onload = function() {
//    console.log("Student List Document Loaded");
//};

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