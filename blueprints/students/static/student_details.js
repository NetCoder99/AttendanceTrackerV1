function handleReturnClick() {
    console.log("handleReturnClick was invoked.");
    window.location.href = "/students";
}
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