$(document).ready(function() {
    console.log("Students Document ready");

})

// -------------------------------------------------------------------------------
$("#selectStudentPicture").change(function() {
    const baseUri = this.baseURI;
    const badgeNumberLbl = $('#badgeNumberLbl');

    file = this.files[0];
    console.log(file.name);
    if (file) {
    const reader = new FileReader();
    reader.onload = (function(theFile) {
      return function(e) {
        // The base64 string is in e.target.result or reader.result
        const base64String = e.target.result;
        postImageToServer(file.name, base64String);
      };
    })(file);
    reader.readAsDataURL(file);
    };
});

// -------------------------------------------------------------------------------
function postImageToServer(fileName, base64String) {
    console.log("processSavePictureResponse was invoked:" + base64String) ;
    const badgeNumber = $('#badgeNumberLbl').html();
    const dataToSend = {
        'badgeNumber' : badgeNumber,
        'file_name' : fileName,
        'fileBase64': base64String
    };
    $.ajax({
      url: '/save_student_picture',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(dataToSend),
      dataType: 'text',
      success: function(response) {
        processSavePictureResponse(response);
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
      }
    });
}

// -------------------------------------------------------------------------------
function processSavePictureResponse(response) {
    console.log("processSavePictureResponse was invoked.");
    $("#divStudentMessages").html("Image was updated");
    $("#studentImage").attr({
        "src": `${response}`
    });;
}


function handleSelectPicture() {
    console.log("handleSelectPicture was invoked.");
}

function handleFieldBlur(fieldName) {
    console.log("handleFieldBlur was invoked.");
}



