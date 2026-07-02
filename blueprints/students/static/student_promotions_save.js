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
//        displayPromotionHistory(saveResponseDict.badgeNumber);
    }
    else {
        $('#lblPromotionSaveResponse').html(saveResponseDict.message);
        $('#lblPromotionSaveResponse').addClass('text-danger');
    }
}
