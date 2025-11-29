$(document).ready(function() {
    console.log("Schedule document ready");
//    var scheduleClassesTable = $('#scheduleClassesTable').DataTable({
//        columnDefs: [
//            {
//                targets: '_all', // Target all columns
//                className: 'dt-left' // Apply left alignment
//            }
//        ]
//    });
    initializeSchedulesTable();
//    $('#studentClassesTable tbody').on('click', 'tr', function() {
//        console.log(`student row was clicked`);
//        var rowData = studentListTable.row(this).data();
//        processStudentEditClick(rowData[1]);
//    });

})

function initializeSchedulesTable() {
  $('#scheduleClassesTable').DataTable({
    "ordering": false,
    "paging": false,
    "searching": false,
    "processing": true,
    "serverSide": true,
    "pageLength": -1,
    "ajax": {
        "url": "schedule_api", // Replace with your actual API endpoint
        "type": "POST", // Or "GET" depending on your API
        "data": function (d) {  }
    },
    "columns": [
        { "data": "dayName" },
        { "data": "classStartTime" },
        { "data": "classFinisTime" },
        { "data": "className" },
        { "data": "classNum" },
        { "data": "classDayOfWeek" },
    ]
});
}
