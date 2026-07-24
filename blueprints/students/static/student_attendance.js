$(document).ready(function() {
    console.log("Students Attendance ready");
})

async function InitializeStudentAttendanceScreen() {
    const badgeNumber = $('#hdnBadgeNumber').val();
    console.log(`InitializeStudentAttendanceScreen: ${badgeNumber}`);
    getAttendanceData();
}

function getAttendanceData() {
    console.log(`getAttendanceData`);
    const badgeNumber = $('#hdnBadgeNumber').val();
    const dataToSend  = {'badgeNumber' : badgeNumber};
    $.ajax({
      url: '/student_attendance_api',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(dataToSend),
      dataType: 'text',
      success: function(response) {
        processAttendanceResponse(response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
}

function processAttendanceResponse(response) {
    console.log(`processAttendanceResponse: ${JSON.stringify(response)}`);
    responseJson = JSON.parse(response);
    const studentData    = responseJson.studentData;
    const attendanceData = responseJson.attendanceData;

    document.getElementById('lbl_attendance_total_count').innerHTML = responseJson.attendance_total_count
    document.getElementById('lbl_last_promotion_date').innerHTML    = responseJson.last_promotion_date
    document.getElementById('lbl_next_belt_name').innerHTML         = responseJson.next_belt_name
    document.getElementById('lbl_next_stripe_title').innerHTML      = responseJson.next_stripe_title

    const headerMessage  = `Review student attendance for : ${studentData.firstName} ${studentData.lastName}`;
    $('#studentAttendancePageTitle').html(headerMessage);
    processStudentAttendanceRecords(attendanceData);
}

function processStudentAttendanceRecords(attendanceData) {
    console.log(`processAttendanceResponse: ${attendanceData}`);
    const tbodyStudentAttendance = $('#tbodyStudentAttendance');
    for (let i = 0; i < attendanceData.length; i++) {
        console.log(attendanceData[i]);
        const dataRow = getStudentAttendanceRow(attendanceData[i]);
        tbodyStudentAttendance.append(dataRow);
    }
}

function getStudentAttendanceRow(attendanceData) {
    const dataRow = document.createElement("tr");

    const td1 = document.createElement("td");
    td1.textContent = attendanceData.attendance_id;
    dataRow.appendChild(td1);

    const td2 = document.createElement("td");
    td2.textContent = attendanceData.classDayOfWeek;
    dataRow.appendChild(td2);

    const td3 = document.createElement("td");
    td3.textContent = attendanceData.checkinDate;
    dataRow.appendChild(td3);

    const td4 = document.createElement("td");
    td4.textContent = attendanceData.checkinTime;
    dataRow.appendChild(td4);

    const td5 = document.createElement("td");
    td5.textContent = attendanceData.className;
    dataRow.appendChild(td5);

    const td6 = document.createElement("td");
    td6.textContent = attendanceData.appliesPromotion;
    dataRow.appendChild(td6);

    const newAnchor = getFunctionHrefElement(attendanceData.attendance_id);
    const tdLast    = document.createElement("td");
    tdLast.append(newAnchor);
    dataRow.append(tdLast);

    return dataRow;
}

function getFunctionHrefElement(attendance_id) {
    const newAnchor = document.createElement('a');
    newAnchor.href       = '#';
    newAnchor.target     = '_blank'; // Opens in a new tab
    newAnchor.title      = 'Edit';
    newAnchor.innerHTML  = 'Edit';

    newAnchor.onclick = function(event) {
      event.preventDefault();
      console.log(`Edit clicked for attendance_id: ${attendance_id}`);

//      $('#exampleModal').find('#divClassNum').html('');
//      $('#exampleModal').find('#divClassDayOfWeek').html(classDayOfWeek);
//      $('#exampleModal').modal('show');
    };
    return newAnchor;
 }