$(document).ready(function() {
    console.log("Students Details Belts ready");
})

function InitializePromotionsScreen() {
    const badgeNumber = $('#hdnBadgeNumber').val();
    console.log(`InitializePromotionsScreen: ${badgeNumber}`);
    $('#lblPromotionSaveResponse').removeClass('text-success');
    $('#lblPromotionSaveResponse').removeClass('text-danger');
    $('#lblPromotionSaveResponse').html("Awaiting input ...");
    $('#lblPromotionSaveResponse').addClass('text-success');
    displayPromotionHistory(badgeNumber);
}

function displayPromotionHistory(badgeNumber) {
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
    for (let i = 0; i < promotionHistory.length; i++) {
        var newRow = `<tr>
                          <td>${promotionHistory[i].beltTitle}</td>
                          <td>${promotionHistory[i].stripeTitle}</td>
                          <td>${promotionHistory[i].promotionDate}</td>
                      </tr>`;
        tbodyStudentPromotions.append(newRow);
        console.log(promotionHistory[i]);
    }

}

// ----------------------------------------------------------------------------------
document.getElementById('studentBelt').addEventListener('change', function(event) {
    var selectedValue = event.target.value;
    console.log("Belt selected value is: " + selectedValue);
    const dataToSend = {'rankNum':selectedValue};
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
});

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
