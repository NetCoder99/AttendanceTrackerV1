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

$("#btnSave").click(function() {
  console.log("Button save was clicked!");
  event.preventDefault();
  const formData = $(frmClassData).serialize();
  console.log(`formData: ${formData}`);
});



// ------------------------------------------------------------------------
function initializeUpdClassDetailsForm(classModal, classDayOfWeek, classNum) {
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

    classModal.find('#inpStartTime').val(classDetails.classStartTime);
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
    uncheckAllRanks(classModal);
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
    classModal.find('#inpClassName').focus();
}

function setDisableAllFields(classModal, disabledFlag) {
    classModal.find('#inpClassName').prop('disabled', disabledFlag);
    classModal.find('#slctStyleNum').prop('disabled', disabledFlag);
    classModal.find('#slctDayOfWeek').prop('disabled', disabledFlag);
    classModal.find('#inpStartTime').prop('disabled', disabledFlag);
    classModal.find('#inpClassDuration').prop('disabled', disabledFlag);
    classModal.find('#chkWhite').prop('disabled', disabledFlag);
}

function uncheckAllRanks(classModal) {
    classModal.find('#chkWhite').prop("checked", false);
    classModal.find('#chkOrange').prop("checked", false);
    classModal.find('#chkYellow').prop("checked", false);
    classModal.find('#chkBlue').prop("checked", false);
    classModal.find('#chkGreen').prop("checked", false);
    classModal.find('#chkPurple').prop("checked", false);
    classModal.find('#chkBrown').prop("checked", false);
    classModal.find('#chkBlack').prop("checked", false);
}