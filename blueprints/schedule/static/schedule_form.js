// ------------------------------------------------------------------------
$(document).ready(function() {
    console.log("Schedule form document ready");

    $('#exampleModal').on('show.bs.modal', function (event) {
        const classModal     = $('#exampleModal');
        const classDayOfWeek = $('#exampleModal').find('#divClassDayOfWeek').html();
        const classNum       = $('#exampleModal').find('#divClassNum').html();
        console.log(`modal dialog activated for: ${classDayOfWeek}, ${classNum}`);
        if (classNum === '') {
            classModal.find('#lblAddClass').removeClass("removed");
            classModal.find('#updAddClass').addClass("removed");
            initializeNewClassForm(classModal, classDayOfWeek);
        }
        else {
            classModal.find('#lblAddClass').addClass("removed");
            classModal.find('#updAddClass').removeClass("removed");
            initializeUpdClassDetailsForm(classModal, classDayOfWeek, classNum);
        }
    });
})

// ------------------------------------------------------------------------
$("#btnSave").click(function() {
    console.log("Button save was clicked!");
    event.preventDefault();
    const formObject = $(frmClassData);
    const formData   = $(frmClassData).serializeArray();
    const formJson   = JSON.stringify(formData);
    console.log(`formData: ${formJson}`);

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/saveClassDetails_api',
        dataType : 'json',
        data : JSON.stringify(formData),
        success : function(result) {
           processSaveResponse(result);
        },error : function(result){
           console.log(result);
        }
    });
});

// ------------------------------------------------------------------------
$("#btnDelete").click(function() {
  console.log("Button delete was clicked!");
  event.preventDefault();
  $("#divClassPrimaryButtons").addClass('removed');
  $("#divClassConfirmations").removeClass('removed');
});

// ------------------------------------------------------------------------
$("#btnClassConfirmDeleteYes").click(function() {
  event.preventDefault();
  classNum = $("#divClassNum").html();
  console.log(`Button delete was clicked for: ${classNum}`);

  $("#divClassPrimaryButtons").removeClass('removed');
  $("#divClassConfirmations").addClass('removed');
});
$("#btnClassConfirmDeleteNo").click(function() {
  console.log("Button delete was clicked!");
  event.preventDefault();
  $("#divClassPrimaryButtons").removeClass('removed');
  $("#divClassConfirmations").addClass('removed');
});
$('#chkAll').on('change', function() {
    const classModal = $('#exampleModal');
    if ($('#chkAll').prop('checked')) {
        setCheckAllRanks(classModal, true)
    }
    else {
        setCheckAllRanks(classModal, false)
    }
});

// ------------------------------------------------------------------------
function processSaveResponse(result) {
    console.log(`processSaveResponse: ${JSON.stringify(result)}`);

    lblPrimaryMessage = $('#lblPrimaryMessage');
    lblPrimaryMessage.html('');
    lblPrimaryMessage.removeClass('text-danger');
    lblPrimaryMessage.addClass('text-success');

    if (result.validationResults.status === 'ok') {
        lblPrimaryMessage.html(result.validationResults.message);
        lblPrimaryMessage.removeClass('text-danger');
        lblPrimaryMessage.addClass('text-success');
        $('#inpClassName').removeClass('invalid');
        $('#inpStartTime').removeClass('invalid');
        $('#inpClassDuration').removeClass('invalid');
        $('#inpFinisTime').val(result.inpFinisTime.value);
    }
    else {
        // - - - - - - - - - - - - - - - - - - - - - - - - - - -
        inpClassDuration = $('#inpClassDuration');
        if (result.inpClassDuration.status === 'ok') {
            inpClassDuration.removeClass('invalid');
        }
        else {
            inpClassDuration.addClass('invalid');
            inpClassDuration.focus();
            lblPrimaryMessage.html(result.inpClassDuration.message);
            lblPrimaryMessage.addClass('text-danger');
        }
        // - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if (result.inpStartTime.status === 'ok') {
            $('#inpStartTime').removeClass('invalid');
        }
        else {
            $('#inpStartTime').addClass('invalid');
            $('#inpStartTime').focus();
            $('#lblPrimaryMessage').html(result.inpStartTime.message);
            $('#lblPrimaryMessage').addClass('text-danger');
        }
        // - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if (result.inpClassName.status === 'ok') {
            $('#inpClassName').removeClass('invalid');
        }
        else {
            $('#inpClassName').addClass('invalid');
            $('#inpClassName').focus();
            $('#lblPrimaryMessage').html(result.inpClassName.message);
            $('#lblPrimaryMessage').addClass('text-danger');
        }
    }

}

// ------------------------------------------------------------------------
function initializeUpdClassDetailsForm(classModal, classDayOfWeek, classNum) {
    setDisableAllFields(classModal, true);
    classModal.find('#btnDelete').removeClass("removed");

    const dataToSend = {
      classDayOfWeek: classDayOfWeek,
      classNum: classNum
    };
    fetch('/getClassDetails_api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dataToSend)
    })
      .then(
          response => response.json()
      )
      .then(
          data => processClassDetails(classModal, data.data)
      )
      .catch(error => console.error('Error:', error));
    }

// ------------------------------------------------------------------------
function processClassDetails(classModal, classDetails) {
    console.log(`processClassDetails: ${classDetails}`);
    classModal.find('#inpClassName').val(classDetails.className);
    classModal.find('#slctStyleNum').val(classDetails.styleNum);
    classModal.find('#slctDayOfWeek').val(classDetails.classDayOfWeek);

    const regex = /\s*(AM|PM)$/i;
    const classStartTime = classDetails.classStartTime.replace(regex, "");
    classModal.find('#inpStartTime').val(classStartTime);

    if (classDetails.classStartTime.indexOf("AM") > 0) {
        $("#chkAm").prop("checked", true);
    }
    else {
        $("#chkPm").prop("checked", true);
    }

    classModal.find('#inpClassDuration').val(classDetails.classDuration);
    classModal.find('#inpFinisTime').val(classDetails.classFinisTime);

    setAllowedRanksCheckBoxes(classModal, classDetails.allowedRanks);

    classModal.find('#inpAllowedAges').val(classDetails.allowedAges);
    classModal.find('#inpClassName').focus();
    setDisableAllFields(classModal, false);
}

//{
//  "allowedAges": "",
//  "allowedRanks": "1,2,3,4,5,6,7,8",
//  "classCheckInFinis": "10.10",
//  "classCheckinStart": "9.45",
//  "classDayOfWeek": 6,
//  "classDisplayTitle": "Junior and Adult ",
//  "classDuration": 50,
//  "classFinisTime": "10:50 AM",
//  "className": "Junior and Adult ",
//  "classNum": 47,
//  "classStartTime": "10:00 AM",
//  "dayName": "Saturday",
//  "sortKey": 315594000,
//  "styleName": null,
//  "styleNum": 1
//}

// ------------------------------------------------------------------------
function setAllowedRanksCheckBoxes(classModal, allowedRanks) {
    const allowedRanksArray = allowedRanks.split(",");
    setCheckAllRanks(classModal, false);
    for (let i = 0; i < allowedRanksArray.length; i++) {
        console.log(`allowedRank: ${allowedRanksArray[i]}`);
        if (allowedRanksArray[i] === "1") {classModal.find('#chkWhite').prop("checked", true);}
        if (allowedRanksArray[i] === "2") {classModal.find('#chkOrange').prop("checked", true);}
        if (allowedRanksArray[i] === "3") {classModal.find('#chkYellow').prop("checked", true);}
        if (allowedRanksArray[i] === "4") {classModal.find('#chkBlue').prop("checked", true);}
        if (allowedRanksArray[i] === "5") {classModal.find('#chkGreen').prop("checked", true);}
        if (allowedRanksArray[i] === "6") {classModal.find('#chkPurple').prop("checked", true);}
        if (allowedRanksArray[i] === "7") {classModal.find('#chkBrown').prop("checked", true);}
        if (allowedRanksArray[i] === "8") {classModal.find('#chkBlack').prop("checked", true);}
    }
}

// ------------------------------------------------------------------------
function initializeNewClassForm(classModal, classDayOfWeek) {
    classModal.find('#inpClassName').val("");
    classModal.find('#slctStyleNum').val("1");
    classModal.find('#slctDayOfWeek').val(classDayOfWeek);
    classModal.find('#inpStartTime').val("");
    classModal.find("#chkPm").prop("checked", true);
    classModal.find('#inpClassDuration').val("");
    classModal.find('#btnDelete').addClass("removed");
    classModal.find('#inpClassName').focus();
    setCheckAllRanks(classModal, false);
}

// ------------------------------------------------------------------------
function setDisableAllFields(classModal, disabledFlag) {
    classModal.find('#inpClassName').prop('disabled', disabledFlag);
    classModal.find('#slctStyleNum').prop('disabled', disabledFlag);
    classModal.find('#slctDayOfWeek').prop('disabled', disabledFlag);
    classModal.find('#inpStartTime').prop('disabled', disabledFlag);
    classModal.find('#inpClassDuration').prop('disabled', disabledFlag);
    classModal.find('#chkWhite').prop('disabled', disabledFlag);
}

// ------------------------------------------------------------------------
function setCheckAllRanks(classModal, status) {
    classModal.find('#chkWhite').prop("checked", status);
    classModal.find('#chkOrange').prop("checked", status);
    classModal.find('#chkYellow').prop("checked", status);
    classModal.find('#chkBlue').prop("checked", status);
    classModal.find('#chkGreen').prop("checked", status);
    classModal.find('#chkPurple').prop("checked", status);
    classModal.find('#chkBrown').prop("checked", status);
    classModal.find('#chkBlack').prop("checked", status);
}

