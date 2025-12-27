$(document).ready(function() {
    console.log("Student Main Document ready");

    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    var studentSearchTabTrigger = document.querySelector('#tabStudentSearch')
    studentSearchTabTrigger.addEventListener('show.bs.tab', function (event) {
        //const badgeNumber = activeTab.setAttribute('data-badge-number', '');
        //console.log(`studentSearchTabTrigger badgeNumber: ${badgeNumber}`);
        console.log(`studentSearchTabTrigger`);
        var activeTab = event.target;
        $("#hdnBadgeNumber").val('');
        $('#tabStudentDetails').prop('disabled', true);
        $('#tabStudentPromotions').prop('disabled', true);
        $('#tabStudentAttendance').prop('disabled', true);
        InitializeStudentsList();
    })

    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    var studentDetailsTabTrigger = document.querySelector('#tabStudentDetails')
    studentDetailsTabTrigger.addEventListener('show.bs.tab', function (event) {
        var activeTab = event.target;
        const badgeNumber = $('#hdnBadgeNumber').val();
        //console.log(`studentDetailsTabTrigger-badgeNumber: ${badgeNumber}`);
        processStudentDetailsLoad(badgeNumber);
    })

    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    var studentPromotionsTabTrigger = document.querySelector('#tabStudentPromotions')
    studentPromotionsTabTrigger.addEventListener('show.bs.tab', function (event) {
        var activeTab = event.target;
        const badgeNumber = $('#hdnBadgeNumber').val();
        console.log(`studentPromotionsTabTrigger-badgeNumber: ${badgeNumber}`);
        InitializePromotionsScreen(badgeNumber);
    })

})

// -----------------------------------------------------------
function handleFieldBlur(fieldName) {
      console.log(`handleFieldBlur: ${fieldName}`);
}

// -----------------------------------------------------------
function handleDetailsClick() {
    console.log("handleDetailsClick was invoked.");
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    window.location.href = "/student_details?badgeNumber="+urlParams.get('badgeNumber');
}
function handlePromotionsClick() {
    console.log("handlePromotionsClick was invoked.");
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    window.location.href = "/student_promotions?badgeNumber="+urlParams.get('badgeNumber');
}
function handleAttendanceClick() {
    console.log("handleAttendanceClick was invoked.");
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    window.location.href = "/student_attendance?badgeNumber="+urlParams.get('badgeNumber');
}