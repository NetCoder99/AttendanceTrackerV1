$(document).ready(function() {
    console.log("Belts list document ready");
    initializeRanksTables();
})

$('#ranks-table-container').on('click', '.slctAddNewStripe', function() {
    console.log("Dynamically created element clicked!");
    console.log("Clicked element ID:", $(this).attr('id'));
});

// ---------------------------------------------------------------------
const ranksTables = [];
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
function initializeRanksTables() {
fetch('getRanksList_api')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(ranksData => {
    processRanksData(ranksData['data']);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function processRanksData(ranksData) {
    for (let i = 0; i < ranksData.length; i++) {
        console.log(`processing rankEntry: ${ranksData[i].rankNum, ranksData[i].rankName}`)
        const rankTable = getRankTable(ranksData[i]);
    }
}

function getRankTable(rankData) {
    console.log(`getRankTable: ${rankData.rankNum}`);
    const $tableObj = $('<table></table');
    $tableObj.attr('id', `ranksTable${rankData.rankNum}`);
    $tableObj.addClass("table table-bordered table-striped w-75 mx-auto")
    const $tableHead = $('<thead></thead');
    const $headerRow = $('<tr></tr>');
    const $rankImage = $('<img />', {
          id:  `rankImage${rankData.rankNum}`,
          src: `static/images/belt_images/${rankData.imageSource}`,
          height: '50px',
          alt: rankData.rankName
    });
    $rankImage.addClass("float-start");
    const $rankHeader = (`<h4 class="d-inline-block fw-bold mt-2 ms-5">${rankData.rankName}</h4>`);
    const $th1 = $(`<th colspan="3"></th>`);
    $th1.append($rankImage);
    $th1.append($rankHeader);
    $headerRow.append($th1);
    $tableHead.append($headerRow);
    $tableObj.append($tableHead);
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    addBeltStripeRows($tableObj, rankData);
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    $('#ranks-table-container').append($tableObj);
    return $tableObj
}

function addBeltStripeRows($tableObj, rankData) {
    console.log(`addBeltStripeRows: ${rankData.rankNum}`);
    fetch('getStripesList_api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(rankData)
    })
    .then(response => response.json())
    .then(stripeData => buildStripesRows($tableObj, rankData, stripeData['data']))
    .catch(error => console.error('Error:', error));
}

function buildStripesRows($tableObj, rankData, stripeData) {
    console.log(`buildStripesRows: ${JSON.stringify(stripeData)}`);
    const tbody = $('<tbody></tbody');
    for (let i = 0; i < stripeData.length; i++) {
        const tr = $('<tr></tr>');
        console.log(`processing stripeEntry: ${stripeData[i].stripeId, stripeData[i].stripeName}`)
        const td1 = $('<td></td>');
        td1.append(GetStripeNameInputBox(stripeData[i]));
        tr.append(td1);
        const td2 = $('<td></td>');
        td2.append(GetStripeClassCount(stripeData[i]));
        tr.append(td2);
        const td3 = $('<td></td>');
        td3.append($('<img src="static/images/icons/plus-square.svg" style="cursor:pointer;" title="Save" class="">'));
        td3.append($('<img src="static/images/icons/trash.svg" style="cursor:pointer;" title="Save" class="ms-2">'));
        tr.append(td3);
        tbody.append(tr);
    }
    const trAddStripe = $('<tr></tr>');
    trAddStripe.append(GetNewStripeCell(rankData));
    tbody.append(trAddStripe);
    $tableObj.append(tbody);
}

function GetStripeNameInputBox(stripeData) {
    const rtnInput = $(`<input type="text"
              id=inpStripe${stripeData.rankNum}_${stripeData.seqNum}
              name=inpStripe${stripeData.rankNum}_${stripeData.seqNum}
              disabled
    />`)
    rtnInput.val(stripeData.stripeName);
    return rtnInput;
}
function GetStripeClassCount(stripeData) {
    const rtnInput = $(`<input type="text"
          id=inpClassCount${stripeData.rankNum}_${stripeData.seqNum}
          name=inpClassCount${stripeData.rankNum}_${stripeData.seqNum}
          style="width: 50px;"
          disabled
    />`)
    rtnInput.val(stripeData.stripeClassCount);
    return rtnInput;
}
function GetFunctionsRow(stripeData) {
    const rtnInput = $(`<input type="text"
          id=inpClassCount${stripeData.rankNum}_${stripeData.seqNum}
          name=inpClassCount${stripeData.rankNum}_${stripeData.seqNum}
          style="width: 50px;"
          disabled
    />`)
    rtnInput.val(stripeData.stripeClassCount);
    return rtnInput;
}
function GetNewStripeCell(rankData) {
    const td3 = $(`<td id="td${rankData.rankName}" colspan="3" class=""></td>`);
    const lnkBtn = $(`<button id=btnRank${rankData.rankNum} class="btn btn-link slctAddNewStripe"></button>`)
    lnkBtn.text(`Add new ${rankData.rankName} stripe`)
    td3.append(lnkBtn);
    return td3;
}

