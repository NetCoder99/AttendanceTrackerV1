$(document).ready(function() {
    console.log("Belts list document ready");
    //initializeDemoTable();
    initializeRanksTables();
})

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
    $('#ranks-table-container').append($tableObj);
    return $tableObj

}

function initializeDemoTable() {
    var tableData = [
        { name: "Alice", age: 30, city: "New York" },
        { name: "Bob", age: 24, city: "London" },
        { name: "Charlie", age: 35, city: "Paris" }
    ];

    // Create the table element
    var $table = $('<table>');
    $table.attr('border', '1'); // Add a border for visibility

    // Create the table header
    var $thead = $('<thead>');
    var $headerRow = $('<tr>');
    $headerRow.append('<th>Name</th>');
    $headerRow.append('<th>Age</th>');
    $headerRow.append('<th>City</th>');
    $thead.append($headerRow);
    $table.append($thead);

    // Create the table body and add rows
    var $tbody = $('<tbody>');
    $.each(tableData, function(index, item) {
        var $row = $('<tr>');
        $row.append('<td>' + item.name + '</td>');
        $row.append('<td>' + item.age + '</td>');
        $row.append('<td>' + item.city + '</td>');
        $tbody.append($row);
    });
    $table.append($tbody);

    // Append the created table to the container
    $('#table-container').append($table);
}


function initializeBeltsTables() {
fetch('getBeltsList_api')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(classData => {
    processBeltsData(classData['data']);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function processBeltsData(beltsData) {
    for (let i = 0; i < 7; i++) {
        console.log(`processing beltsData: ${i}`)
    }
}