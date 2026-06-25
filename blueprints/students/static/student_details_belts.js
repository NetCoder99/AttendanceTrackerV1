$(document).ready(function() {
    console.log("Students Details Belts ready");
})

function InitializePromotionsScreen() {
    console.log('InitializePromotionsScreen');
    const badgeNumber = $('#hdnBadgeNumber').val();
    console.log(`InitializePromotionsScreen: ${badgeNumber}`);
    $('#lblPromotionSaveResponse').removeClass('text-success');
    $('#lblPromotionSaveResponse').removeClass('text-danger');
    $('#lblPromotionSaveResponse').html("Awaiting input ...");
    $('#lblPromotionSaveResponse').addClass('text-success');
    displayPromotionHistory(badgeNumber);
    displayCurrentRankAndStripe(badgeNumber);
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
        var newRow = `<tr>
                          <td>${promotionHistory[i].beltTitle}</td>
                          <td>${promotionHistory[i].stripeTitle}</td>
                          <td>
                            <input type="date" id="start-date" name="trip-start" value=${promotionHistory[i].promotionDate} >
                          </td>
                      </tr>`;
        tbodyStudentPromotions.append(newRow);
    }
}

function setBeltSelectionDropdowns(promotionHistory) {
    console.log("setBeltSelectionDropdowns: " + promotionHistory);
    const selectBeltElement   = $('#studentBelt');
    const selectStripeElement = $('#studentBeltStripes');

    $('#studentBelt').val($('#studentBelt option:first').val())
    $('#studentBeltStripes').val($('#studentBeltStripes option:first').val())

    if (promotionHistory.length == 0) {
        $('#studentBelt').val($('#studentBelt option:first').val())
        $('#studentBeltStripes').val($('#studentBeltStripes option:first').val())
        updateStripeDropdownForRankChange($('#studentBelt').val());

        //$('#studentBelt')[0].selectedIndex = 0;
        //$('#studentBeltStripes')[0].selectedIndex = 0;
    }
    else {
        $('#studentBelt').val(promotionHistory[0].beltId);
        updateStripeDropdownForRankChange($('#studentBelt').val());
    }
}


// ----------------------------------------------------------------------------------
document.getElementById('studentBelt').addEventListener('change', function(event) {
    var rankNum = event.target.value;
    console.log("Belt selected value is: " + rankNum);
    updateStripeDropdownForRankChange(rankNum);
});

function updateStripeDropdownForRankChange(rankNum) {
    console.log("updateStripeDropdownForRankChange: " + rankNum);

    const dataToSend = {'rankNum':rankNum};
    $.ajax({
      url: '/get_stripe_names',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(dataToSend),
      dataType: 'text',
      success: function(response) {
        processSelectRankResponse(response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
}


function processSelectRankResponse(stripeNameRecords) {
    const stripeNamesArray = JSON.parse(stripeNameRecords);
    console.log(`processSelectRankResponse was invoked: ${stripeNamesArray}`);
    const selectElement = $('#studentBeltStripes');
    selectElement.empty();
    for (let i = 0; i < stripeNamesArray.length; i++) {
        console.log(stripeNamesArray[i]);
        $('#studentBeltStripes').append(`<option value=${stripeNamesArray[i].stripeId}>${stripeNamesArray[i].stripeName}</option>`);
    }
}

// ----------------------------------------------------------------------------------
$('#btnPromotionSave').click(function(event) {
    console.log(`btnPromotionSave`);
    event.preventDefault();

    var now = new Date();
    const badgeNumber        = $('#hdnBadgeNumber').val();
    const selectedBeltId     = $("#studentBelt").val();
    const selectedStripeId   = $("#studentBeltStripes").val();
    const selectedBeltName   = $("#studentBelt option:selected").text();
    const selectedStripeName = $("#studentBeltStripes option:selected").text();

    const dataToSend = {
        'badgeNumber'   : badgeNumber,
        'beltId'        : selectedBeltId,
        'beltTitle'     : selectedBeltName,
        'stripeId'      : selectedStripeId,
        'stripeTitle'   : selectedStripeName,
        'studentName'   : null,
        'promotionDate' : now.toLocaleString().replace(/,/g, '')
    };
    console.log(`btnPromotionSave, ${selectedBeltId} : ${selectedStripeId}`);
    $.ajax({
      url: '/upd_student_rank',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(dataToSend),
      dataType: 'text',
      success: function(response) {
        processSaveRankResponse(response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
});

function processSaveRankResponse(saveResponse) {
    const saveResponseDict = JSON.parse(saveResponse);
    console.log(`processSaveRankResponse was invoked: ${saveResponseDict}`);
    $('#lblPromotionSaveResponse').removeClass('text-success');
    $('#lblPromotionSaveResponse').removeClass('text-danger');
    if (saveResponseDict.status == 'ok') {
        $('#lblPromotionSaveResponse').html("Student rank was updated, new id is: " + saveResponseDict.lastRowId);
        $('#lblPromotionSaveResponse').addClass('text-success');
        displayPromotionHistory(saveResponseDict.badgeNumber);
    }
    else {
        $('#lblPromotionSaveResponse').html(saveResponseDict.message);
        $('#lblPromotionSaveResponse').addClass('text-danger');
    }
}

function displayCurrentRankAndStripe(badgeNumber) {
    console.log(`displayCurrentRankAndStripe was invoked: ${badgeNumber}`);
    const dataToSend  = {'badgeNumber' : badgeNumber};
    $.ajax({
      url: '/get_promotion_history',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(dataToSend),
      dataType: 'text',
      success: function(response) {
        console.log("displayCurrentRankAndStripe responded");
        setCurrentRankAndStripeDropdowns(response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });

}

function setCurrentRankAndStripeDropdowns(promotionHistory) {
    const promotionHistoryList = JSON.parse(promotionHistory);
    console.log(`setCurrentRankAndStripeDropdowns was invoked: ${promotionHistoryList}`);
    const textToFind = promotionHistoryList[0].stripeTitle;
    const dropdown = document.getElementById('studentBeltStripes');
//    // Find the index where the option text matches exactly
    const targetIndex = [...dropdown.options].findIndex(option => option.text === textToFind);
    console.log(`setCurrentRankAndStripeDropdowns:targetIndex: ${targetIndex}`);
//    // Set the dropdown to that index if found
    if (targetIndex !== -1) {
      dropdown.selectedIndex = targetIndex;
    }
}