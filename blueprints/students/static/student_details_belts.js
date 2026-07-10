$(document).ready(function() {
    console.log("Students Details Belts ready");
})

//--------------------------------------------------------------------------
function InitializePromotionsScreen() {
    console.log('InitializePromotionsScreen');
    const badgeNumber = $('#hdnBadgeNumber').val();
    console.log(`InitializePromotionsScreen: ${badgeNumber}`);
    $('#lblPromotionSaveResponse').removeClass('text-success');
    $('#lblPromotionSaveResponse').removeClass('text-danger');
    $('#lblPromotionSaveResponse').html("Awaiting input ...");
    $('#lblPromotionSaveResponse').addClass('text-success');
    const promotionDate = document.getElementById('studentPromotionDate');
    promotionDate.valueAsDate = new Date()
    displayStudentDetails(badgeNumber);
    displayPromotionHistory(badgeNumber);
}

function displayStudentDetails(badgeNumber) {
    // get stripes relevant to the student



    console.log(`displayStudentDetails:${badgeNumber} `);
    const dataToSend  = {'badgeNumber' : badgeNumber};
    $.ajax({
      url: '/get_student_details',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(dataToSend),
      dataType: 'text',
      success: function(response) {
        processStudentPromotionDetails(response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
}

function processStudentPromotionDetails(student_details) {
    //console.log(`processStudentPromotionDetails:${student_details}`);
    student_details_json = JSON.parse(student_details);

    const hdrStudentPromotionTitle     = document.getElementById('hdrStudentPromotionTitle');
    hdrStudentPromotionTitle.innerText = `Manage promotions for - ${student_details_json.firstName} ${student_details_json.lastName}`;

    const studentBeltNames     = document.getElementById('studentBeltNames');
    const studentBeltStripes   = document.getElementById('studentBeltStripes');
    const studentPromotionDate = document.getElementById('studentPromotionDate');

    // check if the student has a rank, if not set to white with no stripes
    if (!student_details_json.currentRankNum || (typeof student_details_json.currentRankNum === 'string' && student_details_json.currentRankNum.trim() === '')) {
        studentBeltNames.selectedIndex = 0;
        studentBeltStripes.selectedIndex = 0;
    } else {
        const beltTargetIndex = [...studentBeltNames.options].findIndex(option => option.text === student_details_json.currentRankName);
        studentBeltNames.selectedIndex = beltTargetIndex;
        console.log(`updating stripes dropdown for :${student_details_json.currentRankNum}`);
        // Trigger a POST request to your Python server manually
        htmx.ajax('POST', '/getStripes_htmx', {
            target: '#studentBeltStripes', // Element where the returned HTML goes
            swap: 'innerHTML',          // How to insert the HTML snippet
            values: { rankNum: student_details_json.currentRankNum } // Data passed to Python backend
        })
        .then(function() {
            console.log(`stripes dropdown was updated for :${student_details_json.currentRankNum} : ${student_details_json.currentStripeId}`);
            for (const option of studentBeltStripes.options) {
                console.log(`option is ${option.text} : value is ${option.value}`);
                if (student_details_json.currentStripeId === Number(option.value)) {
                    console.log(`${option.text} : ${option.value} : was found!`);
                    studentBeltStripes.selectedIndex = option.index;
                }
            }
        });
    }

//    console.log(`processStudentPromotionDetails: setting default values`);
//    studentBeltNames.selectedIndex = 0;
//    studentBeltStripes.selectedIndex = 0;
//    studentPromotionDate.valueAsDate = new Date();

//    // Find the index where the option text matches exactly
//    const targetIndex = [...studentBeltNames.options].findIndex(option => option.text === student_details_json.currentRankName);
//    if (targetIndex !== -1) {
//      studentBeltNames.selectedIndex = targetIndex;
//    } else {
//        console.log(`processStudentPromotionDetails: setting default values`);
//        studentBeltNames.selectedIndex = 0;
//        studentBeltStripes.selectedIndex = 0;
//        studentPromotionDate.valueAsDate = new Date();
//    }
//
//

}

//--------------------------------------------------------------------------

function getDisplayableDate() {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
}

function displayPromotionHistory(badgeNumber) {
    console.log(`displayPromotionHistory:${badgeNumber}`);
    const dataToSend  = {'badgeNumber' : badgeNumber};
    $.ajax({
      url: '/get_promotion_history',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(dataToSend),
      dataType: 'text',
      success: function(response) {
        processGetPromotionsResponse(response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
}

function processGetPromotionsResponse(response) {
    console.log("processGetPromotionsResponse");
    promotionHistory = JSON.parse(response);
    const tbodyStudentPromotions = $('#tblStudentPromotions tbody');
    tbodyStudentPromotions.empty();
    //setBeltSelectionDropdowns(promotionHistory);
    for (let i = 0; i < promotionHistory.length; i++) {
        const inpPromotionDate = document.createElement('input');
        inpPromotionDate.type = 'date';
        inpPromotionDate.id = 'dynamic-date';
        inpPromotionDate.name = 'appointment-date';
        const tdPromotionDate = document.createElement('td')
        tdPromotionDate.appendChild(inpPromotionDate);
        const buttonId = `save_promotion_date_${promotionHistory[i].promotionId}`
        var newRow = `<tr>
                          <td>${promotionHistory[i].beltTitle}</td>
                          <td>${promotionHistory[i].stripeTitle}</td>
                          <td>
                            <input type="date" id="promotion-date-inp-${promotionHistory[i].promotionId}" name="promotion-date-inp-${promotionHistory[i].promotionId}" value=${promotionHistory[i].promotionDate} >
                          </td>
                          <td>
                            <button type  = "button"
                                    id    = "save-${buttonId}"
                                    class = "btn btn-sm btn-success"
                                    onclick = "savePromotionDate(${promotionHistory[i].promotionId})">
                                Save
                            </button>
                            <button type  = "button"
                                    id    = "del-${buttonId}"
                                    class = "btn btn-sm btn-success"
                                    onclick = "delPromotionDate(${promotionHistory[i].promotionId})">
                                Del
                            </button>
                          </td>
                          <td>
                            <label id="promotion-response_${promotionHistory[i].promotionId}"></label>
                          </td>
                      </tr>`;
        tbodyStudentPromotions.append(newRow);
    }
}

//function setBeltSelectionDropdowns(promotionHistory) {
//    console.log("setBeltSelectionDropdowns: " + promotionHistory);
//    const selectBeltElement   = $('#studentBelt');
//    const selectStripeElement = $('#studentBeltStripes');
//
//    $('#studentBelt').val($('#studentBelt option:first').val())
//    $('#studentBeltStripes').val($('#studentBeltStripes option:first').val())
//
//    if (promotionHistory.length == 0) {
//        $('#studentBelt').val($('#studentBelt option:first').val())
//        $('#studentBeltStripes').val($('#studentBeltStripes option:first').val())
//        updateStripeDropdownForRankChange($('#studentBelt').val());
//
//        //$('#studentBelt')[0].selectedIndex = 0;
//        //$('#studentBeltStripes')[0].selectedIndex = 0;
//    }
//    else {
//        $('#studentBelt').val(promotionHistory[0].beltId);
//        updateStripeDropdownForRankChange($('#studentBelt').val());
//    }
//}


//// ----------------------------------------------------------------------------------
//document.getElementById('studentBelt').addEventListener('change', function(event) {
//    var rankNum = event.target.value;
//    console.log("Belt selected value is: " + rankNum);
//    updateStripeDropdownForRankChange(rankNum);
//});

//function updateStripeDropdownForRankChange(rankNum) {
//    console.log("updateStripeDropdownForRankChange: " + rankNum);
//
//    const dataToSend = {'rankNum':rankNum};
//    $.ajax({
//      url: '/get_stripe_names',
//      type: 'POST',
//      contentType: 'application/json',
//      data: JSON.stringify(dataToSend),
//      dataType: 'text',
//      success: function(response) {
//        processSelectRankResponse(response);
//      },
//      error: function(xhr, status, error) {
//        console.error('Error:', error);
//      }
//    });
//}


//function processSelectRankResponse(stripeNameRecords) {
//    const stripeNamesArray = JSON.parse(stripeNameRecords);
//    console.log(`processSelectRankResponse was invoked: ${stripeNamesArray}`);
//    const selectElement = $('#studentBeltStripes');
//    selectElement.empty();
//    for (let i = 0; i < stripeNamesArray.length; i++) {
//        console.log(stripeNamesArray[i]);
//        $('#studentBeltStripes').append(`<option value=${stripeNamesArray[i].stripeId}>${stripeNamesArray[i].stripeName}</option>`);
//    }
//}
//
//
//function displayCurrentRankAndStripe(badgeNumber) {
//    console.log(`displayCurrentRankAndStripe was invoked: ${badgeNumber}`);
//    const dataToSend  = {'badgeNumber' : badgeNumber};
//    $.ajax({
//      url: '/get_promotion_history',
//      type: 'POST',
//      contentType: 'application/json',
//      data: JSON.stringify(dataToSend),
//      dataType: 'text',
//      success: function(response) {
//        console.log("displayCurrentRankAndStripe responded");
//        setCurrentRankAndStripeDropdowns(response);
//      },
//      error: function(xhr, status, error) {
//        console.error('Error:', error);
//      }
//    });
//
//}
//
//function setCurrentRankAndStripeDropdowns(promotionHistory) {
//    const promotionHistoryList = JSON.parse(promotionHistory);
//    console.log(`setCurrentRankAndStripeDropdowns was invoked: ${promotionHistoryList}`);
//    const textToFind = promotionHistoryList[0].stripeTitle;
//    const dropdown = document.getElementById('studentBeltStripes');
////    // Find the index where the option text matches exactly
//    const targetIndex = [...dropdown.options].findIndex(option => option.text === textToFind);
//    console.log(`setCurrentRankAndStripeDropdowns:targetIndex: ${targetIndex}`);
////    // Set the dropdown to that index if found
//    if (targetIndex !== -1) {
//      dropdown.selectedIndex = targetIndex;
//    }
//}