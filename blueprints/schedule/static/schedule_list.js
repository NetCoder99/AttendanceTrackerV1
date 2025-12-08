$(document).ready(function() {
    console.log("Schedule document ready");
    initializeSchedulesTable();
})

function initializeSchedulesTable() {
fetch('schedule_api')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(classData => {
    processScheduleData(classData['data']);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function processScheduleData(classData) {
    let prevDayOfWeek = -1;
    const classTable = $("#classTable");

    for (let i = 0; i < 7; i++) {
        //console.log(`processing classDayOfWeek: ${i}`)
        const dailyRecords = classData.filter(classDataRec => classDataRec.classDayOfWeek === i);
        //console.log(`class count: ${dailyRecords.length}`)
        const tableHeader = getDailyTableHeader(i);
        addTableHeaderContent(i, tableHeader);
        const tableBody   = getDailyTableBody(i);
        addTableBodyContent(i, dailyRecords, tableBody);
    }
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

function addTableBodyContent(classDayOfWeek, dailyRecords, tableBody) {
    try {
        if (tableBody === null) {
            console.log('table body was null');
            throw `Table body was null: ${classDayOfWeek}`;
        }
        //const dailyRecords = classData.filter(classDataRec => classDataRec.classDayOfWeek === classDayOfWeek);
        //console.log(`dailyRecord size: ${dailyRecords.length}`);
        for (let i = 0; i < dailyRecords.length; i++) {
            //console.log(`dailyRecord: ${dailyRecords[i].classDayOfWeek} - ${dailyRecords[i].className}`);
            addTableBodyRow(tableBody, dailyRecords[i]);
        }
        addTableBodyAddClassRow(tableBody, classDayOfWeek);
    } catch (error) {
        console.error("An error occurred:", error.message);
    }
}

function addTableBodyRow(tableBody, classRecord) {
    try {
        if (tableBody === null) {
            console.log('table body was null');
        }
        const dataRow = document.createElement("tr");

        const td1 = document.createElement("td");
        td1.style.width = '30rem';
        td1.textContent = classRecord.className;
        td1.classList.add('border-bottom-0');
        dataRow.appendChild(td1);

        const td2 = document.createElement("td");
        td2.textContent = classRecord.classStartTime;
        td2.classList.add('border-bottom-0');
        dataRow.appendChild(td2);

        const td3 = document.createElement("td");
        td3.textContent = classRecord.classFinisTime;
        td3.classList.add('border-bottom-0');
        dataRow.appendChild(td3);

        const td4 = document.createElement("td");
        td4.textContent = classRecord.styleName;
        td4.classList.add('border-bottom-0');
        dataRow.appendChild(td4);

        const newAnchor = document.createElement('a');
        newAnchor.href = '#';
        newAnchor.target = '_blank'; // Opens in a new tab
        newAnchor.title = 'Edit';
        newAnchor.innerHTML  = 'Edit';
        newAnchor.onclick = function(event) {
          event.preventDefault();
          $('#exampleModal').find('#divClassNum').html(classRecord.classNum);
          $('#exampleModal').find('#divClassDayOfWeek').html(classRecord.classDayOfWeek);
          $('#exampleModal').modal('show');

          console.log(`Edit clicked for classNum: ${classRecord.classNum}`);
        };

        const td5 = document.createElement("td");
        td5.append(newAnchor);
        td5.classList.add('border-bottom-0');
        dataRow.appendChild(td5);

        tableBody.append(dataRow);
    } catch (error) {
        console.error("An error occurred:", error.message);
    }
}


function addTableBodyAddClassRow(tableBody, classDayOfWeek) {
    try {
        if (tableBody === null) {
            console.log('table body was null');
        }
        const dataRow = document.createElement("tr");
        const newAnchor = document.createElement('a');
        newAnchor.href = '#';
        newAnchor.target = '_blank'; // Opens in a new tab
        newAnchor.title = 'Add new class';
        newAnchor.innerHTML  = 'Add new class';

        newAnchor.onclick = function(event) {
          event.preventDefault();
          $('#exampleModal').find('#divClassNum').html('');
          $('#exampleModal').find('#divClassDayOfWeek').html(classDayOfWeek);
          $('#exampleModal').modal('show');
        };

        const td1 = document.createElement("td");
        td1.append(newAnchor);
        td1.colSpan = 5;
        dataRow.appendChild(td1);
        tableBody.append(dataRow);
    } catch (error) {
        console.error("An error occurred:", error.message);
    }
}

function getDailyTableBody(classDayOfWeek) {
    switch(classDayOfWeek) {
        case 0: return $('#tbodyClassSunday');
        case 1: return $('#tbodyClassMonday');
        case 2: return $('#tbodyClassTuesday');
        case 3: return $('#tbodyClassWednesday');
        case 4: return $('#tbodyClassThursday');
        case 5: return $('#tbodyClassFriday');
        case 6: return $('#tbodyClassSaturday');
        default: throw `Unknown classDayOfWeek: ${classDayOfWeek}`;
    }
}

function getDailyTableHeader(classDayOfWeek) {
    switch(classDayOfWeek) {
        case 0: return $('#theadClassSunday');
        case 1: return $('#theadClassMonday');
        case 2: return $('#theadClassTuesday');
        case 3: return $('#theadClassWednesday');
        case 4: return $('#theadClassThursday');
        case 5: return $('#theadClassFriday');
        case 6: return $('#theadClassSaturday');
        default: throw `Unknown classDayOfWeek: ${classDayOfWeek}`;
    }
}

function addTableHeaderContent(classDayOfWeek, tableHeader) {
    try {
        if (tableHeader === null) {
            console.log('table header was null');
        }
        const headerRow = document.createElement("tr");
        const th1 = document.createElement("th");
        th1.style.width = '20rem';
        th1.textContent = 'Class Name';
        headerRow.appendChild(th1);
        const th2 = document.createElement("th");
        th2.textContent = 'Start Time';
        headerRow.appendChild(th2);
        const th3 = document.createElement("th");
        th3.textContent = 'End Time';
        headerRow.appendChild(th3);
        const th4 = document.createElement("th");
        th4.textContent = 'Style Name';
        headerRow.appendChild(th4);
        const th5 = document.createElement("th");
        th5.textContent = 'Function';
        headerRow.appendChild(th5);
        tableHeader.append(headerRow);
    } catch (error) {
        console.error("An error occurred:", error.message);
    }
}

