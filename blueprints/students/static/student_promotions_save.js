$(document).ready(function() {
    console.log("student_promotions_save ready");
})


// ----------------------------------------------------------------------------------
function fncPromotionSave() {
    console.log(`fncPromotionSave`);
    event.preventDefault();

    var now = new Date();
    const badgeNumber        = $('#hdnBadgeNumber').val();
    const selectedBeltId     = $("#studentBeltNames").val();
    const selectedStripeId   = $("#studentBeltStripes").val();
    const selectedBeltName   = $("#studentBeltNames option:selected").text();
    const selectedStripeName = $("#studentBeltStripes option:selected").text();
    const studentPromotionDate = $("#studentPromotionDate").val();

    const dataToSend = {
        'badgeNumber'   : badgeNumber,
        'beltId'        : selectedBeltId,
        'beltTitle'     : selectedBeltName,
        'stripeId'      : selectedStripeId,
        'stripeTitle'   : selectedStripeName,
        'studentName'   : null,
        'promotionDate' : studentPromotionDate.replace(/,/g, '')
    };
    console.log(`fncPromotionSave, ${badgeNumber} : ${selectedBeltId} : ${selectedStripeId} : ${studentPromotionDate}`);
    console.log(`fncPromotionSave, ${JSON.stringify(dataToSend)}`);

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
};

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

function savePromotionDate(promotionId) {
    console.log(`savePromotionDate was invoked: ${promotionId}`);
    const promotionDateBoxId = `#promotion-date-inp-${promotionId}`
    const promotionDateBox   = $(promotionDateBoxId)
    htmx.ajax('POST', '/save_promotion_date', {
        target: '#lblPromotionSaveResponse', // Where the backend HTML goes
        swap: 'innerHTML',     // How to replace the content
        values: { promotionId: promotionId, promotionDate: promotionDateBox.val()} // Data payload
    }).then(() => {
        setTimeout(() => {
            $('#lblPromotionSaveResponse').html("Awaiting input ...");
        }, 4000);
    });
}

function delPromotionRecord(promotionId){
    console.log(`delPromotionRecord was invoked: ${promotionId}`);
    const badgeNumber        = $('#hdnBadgeNumber').val();
    $.ajax({
      url: '/del_promotion_record',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({'promotionId' : promotionId, 'badgeNumber': badgeNumber}),
      dataType: 'text',
      success: function(response) {
        processAttendanceDeletion(response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
}

function processAttendanceDeletion(response){
    console.log(`processAttendanceDeletion was invoked: ${response}`);
    responseJson = JSON.parse(response);

    const lblPromotionSaveResponse2     = document.getElementById('lblPromotionSaveResponse')
    lblPromotionSaveResponse2.innerHTML = responseJson.message;
    displayPromotionsHistory(responseJson.promotionHistory);
    setTimeout(() => {
        $('#lblPromotionSaveResponse').html("Awaiting input ...");
    }, 4000);

}

function displayPromotionsHistory(promotionHistory) {
    console.log("displayPromotionsHistory");
    //promotionHistory = JSON.parse(response);
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
                                    onclick = "delPromotionRecord(${promotionHistory[i].promotionId})">
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