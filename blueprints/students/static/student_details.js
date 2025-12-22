$(document).ready(function() {
    console.log("Student Details Document ready");
    $( "#frmBirthDate" ).datepicker();
})

//function handleReturnClick() {
//    console.log("handleReturnClick was invoked.");
//    window.location.href = "/students";
//}

// -----------------------------------------------------------
function processStudentDetailsLoad(badgeNumber) {
    console.log(`processPageLoad: ${badgeNumber}`);
    if (badgeNumber) {
        $("#prgPageTitle").html(`Updating student record - ${badgeNumber}`);
        $('#tabStudentDetails').prop('disabled', false);
        $('#tabStudentPromotions').prop('disabled', false);
        $('#tabStudentAttendance').prop('disabled', false);
        InitializeStudentDetailsFormBadge(badgeNumber);
    }
    else {
        $("#prgPageTitle").html(`Creating new student record.`);
        $('#tabStudentDetails').prop('disabled', true);
        $('#tabStudentPromotions').prop('disabled', true);
        $('#tabStudentAttendance').prop('disabled', true);
    }
}

function InitializeStudentDetailsFormEmpty() {
    console.log("InitializeStudentDetailsFormEmpty");
}

function InitializeStudentDetailsFormBadge(badgeNumber) {
    console.log("InitializeStudentDetailsFormBadge");
    fetch('/student_details_api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'badgeNumber' : badgeNumber})
    })
    .then(response => response.json())
    .then(studentData => DisplayStudentData(studentData))
    .catch(error => console.error('Error:', error));
}

function DisplayStudentData(studentData) {
    console.log(`DisplayStudentData: ${JSON.stringify(studentData)}`);
    const imageDataStr = `data:image/${studentData.studentImageType};base64,${studentData.studentImageBase64}`;
    $("#studentImageTmp").attr("src", imageDataStr);
    $("#studentImageName").html(studentData.studentImageName);
    $('#frmFirstName').val(studentData.firstName);
    $('#frmLastName').val(studentData.lastName);
    $('#frmAddress').val(studentData.address);
    $('#frmAddress2').val(studentData.address2);
    $('#frmCity').val(studentData.city);
    $('#frmState').val(studentData.state);
    $('#frmZip').val(studentData.zip);
    $('#frmBirthDate').val(studentData.birthDate);
    $('#frmPhoneHome').val(studentData.phoneHome);
    $('#frmEmail').val(studentData.email);
}

$('#btnSaveStudentUpdate').off().on('click', function() {

    const badgeNumber = $('#hdnBadgeNumber').val();

    console.log("btnSaveStudentUpdate: Clicked");
    event.preventDefault();
    const formObject = $('#frmStudentDetails');
    let   formData   = $('#frmStudentDetails').serializeArray();
    formData.push({'name': 'badgeNumber', 'value' : badgeNumber});
    const studentJsonData = JSON.stringify(formData);

    fetch('save_student_details_api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })
    .then(response    => response.json())
    .then(studentSaveResponse => ProcessSaveStudentResponse(studentSaveResponse))
    .catch(error      => console.error('Error:', error));
});

function ProcessSaveStudentResponse(studentSaveResponse) {
    console.log(`DisplayStudentSaveResponse: ${JSON.stringify(studentSaveResponse.validationResults)}`);
    const validationStudentResults = studentSaveResponse.validationResults;

    let errorMessage = "";

    for (const [key, value] of Object.entries(studentSaveResponse)) {
      console.log(`${key} is ${value.status} : ${value.message}`);
      const frmField = $(`#${key}`);
      frmField.removeClass("invalid");
      if (value.status == "error") {
        frmField.addClass("invalid");
        if (errorMessage == "") {
            errorMessage = value.message
            frmField.focus();
        }
      }
      else {
          console.log(`Check for reformatted value: ${value}`);
          const rtnFieldName = key.replace(/^frm/, "rtn");
          if (rtnFieldName in value) {
              console.log(`Display formatted value: ${value[rtnFieldName]}`);
              $(`#${key}`).val(value[rtnFieldName]);
          }
      }
    }

    $('#divStudentMessages').removeClass('text-danger');
    $('#divStudentMessages').removeClass('text-success');
    if (errorMessage == "") {
        $('#divStudentMessages').addClass('text-success');
        $('#divStudentMessages').html("Student updates saved");
    }
    else {
        $('#divStudentMessages').addClass('text-danger');
        $('#divStudentMessages').html(errorMessage);
    }


    setTimeout(() => {
        $('#divStudentMessages').html("Awaiting input ...");
        $('#divStudentMessages').removeClass('text-danger');
        $('#divStudentMessages').addClass('text-success');
    }, 5000);
}
