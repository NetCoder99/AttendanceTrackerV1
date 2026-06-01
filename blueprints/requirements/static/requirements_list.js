$(document).ready(function() {
    console.log("Requirements list document ready");
    initializeRequirementsTable();
})

// ---------------------------------------------------------------------
const requirementsTables = [];
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
function initializeRequirementsTable() {
    console.log('initializeRequirementsTable');

    var requirementsListTable = $('#requirementsListTable').DataTable({
        dom: '<"toolbar">frtip',
        pageLength: -1,
        initComplete: function () {
            $('div.toolbar').html('<button id="btnNewRequirement" class="btn btn-success btn-new-student">New Requirement</button>');
            $('#btnNewRequirement').on('click', function() {
                console.log('btnNewRequirement was clicked');
            });
        },
        "ajax": {
            "url": "getRequirementsList_api", // URL of your Python API
            "type": "GET",
            "dataSrc": "data"   // Property in the JSON response
        },
        "columns": [
                { data: 'requirementId' },
                { data: 'beltTitle' },
                { data: 'stripeTitle' },
                { data: 'requiredClasses' }
        ]
    });

}
//
//// ---------------------------------------------------------------------
//$('#requirements-table-container').on('click', '.del-icon', function() {
//    console.log('Delete requirements row, Item id', this.id);
//});
//
//// ---------------------------------------------------------------------
//$('#requirements-table-container').on('click', '.slctAddNewStripe', function() {
//    console.log("Add new requirements row");
//});
//
