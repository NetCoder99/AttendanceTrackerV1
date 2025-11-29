$(document).ready(function() {
    console.log("Students Document ready");

    var studentListTable = $('#studentListTable').DataTable({
        columnDefs: [
            {
                targets: '_all', // Target all columns
                className: 'dt-left' // Apply left alignment

            }
        ]
    });

    $('#studentListTable tbody').on('click', 'tr', function() {
        console.log(`student row was clicked`);
        var rowData = studentListTable.row(this).data();
        processStudentEditClick(rowData[1]);
    });

})

// -------------------------------------------------------------------------------
function processStudentEditClick(badgeNumber) {
    console.log(`processStudentEditClick was invoked: ${badgeNumber}`);
    const badgeNbr = $('#studentBadgeNumber').html();
    window.location.href = `/student_details?badgeNumber=${badgeNumber}`;
}

// -------------------------------------------------------------------------------
function processSearchClick() {
    console.log("processSearchClick was invoked");
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
}

//// -------------------------------------------------------------------------------
//function processSearchResponse(response) {
//    console.log("processSearchResponse was invoked.");
////    let studentListTBbody = $('#studentListTBbody');
////    studentListTBbody.empty()
////    $.each(response, function(index, value) {
////        const row = document.createElement("tr");
////        Object.values(rowData).forEach(value => {
////            const td = document.createElement("td");
////            td.textContent = value;
//////                <td>
//////                    <img id="studentImage"
//////                         src=data:image/{{student_record.studentImageType}};base64,{{student_record.studentImageBase64}}
//////                         alt="No image found"
//////                         height=50
//////                         width=auto
//////                    />
//////                </td>
//////                <td>{{ student_record.badgeNumber }}</td>
//////                <td>{{ student_record.firstName }} {{ student_record.lastName }}</td>
//////                <td>{{ student_record.currentRankName }}</td>
////
////            const td = document.createElement("td");
////            td.textContent = value;
////            row.appendChild(td);
////        });
////        studentListTBbody.appendChild(row);
////
////        student_card.find('#studentBadgeNumber').html(value.badgeNumber);
////    });
//
////    student_card = $('#divStaticCard').find('#divStudentCard');
////    let divStudentsList = $('#divStudentsList');
////    console.log("Student list length - before empty: " + divStudentsList.length);
////    divStudentsList.empty();
////    console.log("Student list length - after empty: " + divStudentsList.length);
////    $.each(response, function(index, value) {
////        student_card.find('#studentBadgeNumber').html(value.badgeNumber);
////        student_card.find('#studentStudentName').html(value.firstName + ' ' + value.lastName);
////        student_card.find('#studentRankName').html(value.currentRankName);
////        student_card.find('#studentImage').attr({
////            "src": `data:image/${value.studentImageType};base64,${value.studentImageBase64}`
////        });
//////        student_card.attr({"id": "divStudentCard_" + value.badgeNumber`});
////        let studentCardNew = student_card.clone(true);
////        divStudentsList.append(student_card.clone(true));
////        console.log("Index: " + index + ", Value: " + value.badgeNumber);
////        console.log("Student list length - during: " + divStudentsList.length);
////    });
////    console.log("Student list length - after: " + divStudentsList.length);
//
//}

