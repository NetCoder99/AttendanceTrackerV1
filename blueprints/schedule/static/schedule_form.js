// ------------------------------------------------------------------------
$(document).ready(function() {
    console.log("Schedule form document ready");

    $('#exampleModal').on('show.bs.modal', function (event) {
        const classModal     = $('#exampleModal');
        const classDayOfWeek = $('#exampleModal').find('#divClassDayOfWeek').html();
        const classNum       = $('#exampleModal').find('#divClassNum').html();
        console.log(`modal dialog activated for: ${classDayOfWeek}, ${classNum}`);
        if (classNum === '') {
            initializeNewClassForm(classModal, classDayOfWeek);
        }
        else {
            initializeUpdClassForm(classModal, classDayOfWeek, classNum);
        }
    });
})

// ------------------------------------------------------------------------
$("#btnSave").click(function() {
    console.log("Button save was clicked!");
    event.preventDefault();
    const formObject = $(frmClassData);
    let   formData   = $(frmClassData).serializeArray();
    classNum = $("#divClassNum").html();
    formData.push({'name': 'classNum', 'value': classNum});
    const formJson   = JSON.stringify(formData);
    console.log(`formData: ${formJson}`);

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/saveClassDetails_api',
        dataType : 'json',
        data : JSON.stringify(formData),
        success : function(result) {
           processSaveResponse(result, classNum);
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
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/deleteClassDetails_api',
        dataType : 'json',
        data : JSON.stringify({'classNum': classNum}),
        success : function(result) {
           processDeleteResponse(result);
        },error : function(result){
           console.log(result);
        }
    });
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
function processDeleteResponse(result) {
    console.log(`processDeleteResponse: ${JSON.stringify(result)}`);
    if (result.status === 'ok') {
        $('#exampleModal').modal('hide');
        location.reload();
    }
    else {
        lblPrimaryMessage = $('#lblPrimaryMessage');
        lblPrimaryMessage.html(result.message);
        lblPrimaryMessage.addClass('text-danger');
        lblPrimaryMessage.removeClass('text-success');
    }
}

// ------------------------------------------------------------------------
function processSaveResponse(result, classNum) {
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
        if (classNum === null) {$('#inpFinisTime').val(result.inpFinisTime.value);}
        $('#exampleModal').modal('hide');
        location.reload();
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
        // - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if (result.classOverLap.status === 'ok') {
            $('#inpClassName').removeClass('invalid');
        }
        else {
            $('#inpStartTime').addClass('invalid');
            $('#inpStartTime').focus();
            $('#lblPrimaryMessage').html(result.classOverLap.message);
            $('#lblPrimaryMessage').addClass('text-danger');
        }
    }

}


// ------------------------------------------------------------------------
function initializeNewClassForm(classModal, classDayOfWeek) {
    classModal.find('#lblAddClass').removeClass("removed");
    classModal.find('#updAddClass').addClass("removed");
    classModal.find('#inpClassName').val("");
    classModal.find('#slctStyleNum').val("1");
    classModal.find('#slctDayOfWeek').val(classDayOfWeek);
    classModal.find('#inpStartTime').val("");
    classModal.find("#chkPm").prop("checked", true);
    classModal.find('#inpClassDuration').val("");
    classModal.find('#btnDelete').addClass("removed");
    classModal.find('#inpClassName').focus();
    setCheckAllRanks(classModal, false);
    setDisableAllFields(classModal, false);
}

// ------------------------------------------------------------------------
function initializeUpdClassForm(classModal, classDayOfWeek, classNum) {
    classModal.find('#lblAddClass').addClass("removed");
    classModal.find('#updAddClass').removeClass("removed");
    classModal.find('#btnDelete').removeClass("removed");
    setDisableAllFields(classModal, true);
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
    .then(response => response.json())
    .then(data => displayClassDetails(classModal, data.data))
    .catch(error => console.error('Error:', error));
}

// ------------------------------------------------------------------------
function displayClassDetails(classModal, classDetails) {
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
    classModal.find('#slctDayOfWeek').prop('disabled', true);
    classModal.find('#inpStartTime').prop('disabled', true);
    classModal.find('#inpClassDuration').prop('disabled', true);
    $('input[name="chkAmPm"]').prop('disabled', true);
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

