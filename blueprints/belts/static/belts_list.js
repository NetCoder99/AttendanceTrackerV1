$(document).ready(function() {
    console.log("Belts list document ready");
    initializeRanksTables();
})

// ---------------------------------------------------------------------
$('#ranks-table-container').on('click', '.del-icon', function() {
    console.log('Delete row, Item id', this.id);

    const rankNum   = this.id.split("_")[1];
    const stripeNum = this.id.split("_")[2];
    const tableId   = `#ranksTable${rankNum}`;
    const trId      = `#inpStripe${rankNum}_${stripeNum}`;

    const table   = $('#ranks-table-container').find(`${tableId}`);
    const tbody   = table.find('tbody');
    const lastRow = tbody.find('tr').last();

    fetch('delStripe_api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'rankNum' : rankNum, 'stripeId' : stripeNum })
    })
    .then(response   => response.json())
    .then(stripeData => ProcessDeleteStripeResponse(tbody, lastRow))
    .catch(error => console.error('Error:', error));
});

function ProcessDeleteStripeResponse(tbody, lastRow) {
    console.log('ProcessDeleteStripeResponse');
    try {
        lastRow.remove();
        const prevRow  = tbody.find('tr').last();
        const prevCell = prevRow.find('td').last();
        const prevImg  = prevCell.find('img');
        prevImg.removeClass('hidden');
    } catch (error) {
        console.error('Error:', error)
    } finally {
      // Code that always runs (cleanup)
    }

}

// ---------------------------------------------------------------------
$('#ranks-table-container').on('click', '.slctAddNewStripe', function() {
    console.log("Add new stripe clicked");
    fetch('addNextStripe_api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'rankNum' : this.id[this.id.length - 1] })
    })
    .then(response   => response.json())
    .then(stripeData => AddNewStripeRow(stripeData))
    .catch(error => console.error('Error:', error));
});

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
function AddNewStripeRow(stripeData) {
    console.log(`AddNewStripeRow: ${stripeData.nextStripeName}, ${stripeData.nextClassCount}`);
    const table = $('#ranks-table-container').find(`#ranksTable${stripeData.rankNum}`);
    const tbody = table.find('tbody');
    const trId  = ``;
    const tr = $(`<tr></tr>`);
    const td1 = $('<td></td>');
    td1.append(GetStripeNameInputBox(stripeData));
    tr.append(td1);
    const td2 = $('<td></td>');
    td2.append(GetStripeClassCount(stripeData));
    tr.append(td2);
    const td3 = $('<td></td>');
    td3.append($(`<img id=delIcon_${stripeData.rankNum}_${stripeData.lastRowId} src="static/images/icons/trash.svg" style="cursor:pointer;" title="Save" class="ms-2 del-icon">`));
    tr.append(td3);
    tbody.append(tr);

    const prevTr = tr.last().prev();
    prevTd   = prevTr.find('td').last();
    prevImg  = prevTd.find('img');
    prevImg.addClass('hidden');
    console.log(`AddNewStripeRow: ${stripeData.nextStripeName}, ${stripeData.nextClassCount}`);

}

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

// ---------------------------------------------------------------------------
// create the ranks/stripes table and add that to the html
// ---------------------------------------------------------------------------
function getRankTable(rankData) {
    console.log(`getRankTable: ${rankData.rankNum}`);
    const $tableObj = $('<table></table');
    $tableObj.attr('id', `ranksTable${rankData.rankNum}`);
    $tableObj.addClass("table table-bordered table-striped w-100 mx-auto")
    const $tableHead = $('<thead></thead');
    const $headerRow = $('<tr></tr>');
    const $rankImage = $('<img />', {
          id:  `rankImage${rankData.rankNum}`,
          src: `static/images/${rankData.imageSource}`,
          height: '75px',
          alt: rankData.rankName
    });

    $rankImage.addClass("float-start");

    const $rankHeader = (`<h4 class="d-inline-block fw-bold mt-2 ms-5">${rankData.rankName}</h4>`);

    const rankStripesLbl = document.createElement('label');
    rankStripesLbl.textContent = 'Max Stripes:';
    rankStripesLbl.className = 'form-label d-inline-block ms-2';
    const rankStripes = document.createElement('input');
    rankStripes.type = 'numeric';
    rankStripes.placeholder = '6';
    rankStripes.style.width = '60px';
    rankStripes.className = 'form-control d-inline-block mb-1 ms-3';
    rankStripes.defaultValue = rankData.stripeCount;
    rankStripes.disabled = true;

    const rankCountLbl = document.createElement('label');
    rankCountLbl.textContent = 'Classes:';
    rankCountLbl.className = 'form-label d-inline-block ms-4';
    const rankCount = document.createElement('input');
    rankCount.type = 'numeric';
    rankCount.placeholder = '6';
    rankCount.style.width = '60px';
    rankCount.className = 'form-control d-inline-block mb-1 ms-3';
    rankCount.defaultValue = rankData.classCount;
    rankCount.disabled = true;

    const rankSaveBtn = document.createElement('button');
    rankSaveBtn.innerText  = 'Save';
    rankSaveBtn.className = 'btn btn-success d-inline-block mb-1 ms-3';
    rankSaveBtn.disabled = true;

    const rankNewStripeBtn = document.createElement('button');
    rankNewStripeBtn.innerText  = 'Add New Stripe';
    rankNewStripeBtn.className = 'btn btn-success d-inline-block mt-3 float-end';
    rankNewStripeBtn.disabled = true;

    const $th1 = $(`<th colspan="3"></th>`);

    $th1.append($rankImage);
    $th1.append($rankHeader);
    $th1.append(rankStripesLbl);
    $th1.append(rankStripes);
    $th1.append(rankCountLbl);
    $th1.append(rankCount);
    $th1.append(rankSaveBtn);
    $th1.append(rankNewStripeBtn);

    const $promotionCount = (`<h4 class="d-inline-block fw-bold mt-2 ms-5">${rankData.rankName}</h4>`);


    $headerRow.append($th1);

//    const $th2 = $(`<th id="td${rankData.rankName}" colspan="1" class=""></th>`);
//    lnkBtn.text(`Add new ${rankData.rankName} stripe`)
//    $th2.append(lnkBtn);
//    $headerRow.append($th2);

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
    .then(stripeData => buildStripesRows($tableObj, stripeData['data']))
    .catch(error => console.error('Error:', error));
}

function buildStripesRows($tableObj, stripeData) {
    console.log(`buildStripesRows: ${JSON.stringify(stripeData)}`);
    const tbody = $('<tbody></tbody');
    for (let i = 0; i < stripeData.length; i++) {
        const trId = `#inpStripe${stripeData[i].RankNumId}_${stripeData[i].RankNumId}`;

        const tr = $(`<tr id=#inpStripe${stripeData[i].RankNumId}_${stripeData[i].RankNumId}></tr>`);
        //console.log(`processing stripeEntry: ${stripeData[i].stripeId, stripeData[i].stripeName}`)
        const td1 = $('<td></td>');
        td1.append(GetStripeNameInputBox(stripeData[i]));
        tr.append(td1);
        const td2 = $('<td></td>');
        td2.append(GetStripeClassCount(stripeData[i]));
        tr.append(td2);
        const td3 = $('<td></td>');
//        td3.append($(`<img id=delIcon_${stripeData[i].rankNum}_${stripeData[i].stripeId} src="static/images/icons/trash.svg" style="cursor:pointer;" title="Save" class="ms-2 del-icon">`));
//        td3.find('img').addClass('hidden');
//        if (!stripeData[i].lastStripeFlag) {
//            td3.find('img').addClass('hidden');
//        }
        tr.append(td3);
        tbody.append(tr);
    }
    $tableObj.append(tbody);
}

function GetStripeNameInputBox(stripeData) {
    const rtnInput = $(`<input type="text"
              id=inpStripe${stripeData.RankNumId}
              name=inpStripe${stripeData.RankNumId}
              disabled
    />`)
    rtnInput.val(stripeData.StripeName);
    return rtnInput;
}
function GetStripeClassCount(stripeData) {
    const rtnInput = $(`<input type="text"
          id=inpClassCount${stripeData.RankNumId}
          name=inpClassCount${stripeData.RankNumId}
          style="width: 50px;"
          disabled
    />`)
    rtnInput.val(stripeData.TotalRequiredClasses);
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

// ------------------------------------------------------------------
$('#btnPrintBeltsPDF').off().on('click', function() {
    console.log("btnPrintBeltsPDF was invoked");
    $.ajax({
      url: '/print_belt_api',
      type: 'POST',
      contentType: 'application/json',
      data: null,
      dataType: 'text',
      success: function(response) {
        processCreateBadgeResponse(response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
})