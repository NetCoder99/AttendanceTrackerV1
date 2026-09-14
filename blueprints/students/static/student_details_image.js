$(document).ready(function() {
    console.log("Students Image ready");
})

// -------------------------------------------------------------------------------
$("#selectStudentPicture").change(function(event) {
    console.log("selectStudentPicture was invoked:") ;
    const file = event.target.files[0]; // Get the first selected file
    console.log(file.name);

    if (file) {
        $("#studentImageName").text(file.name);
        const reader = new FileReader();
        reader.onload = (function(theFile) {
          return function(e) {
            // The base64 string is in e.target.result or reader.result
            const base64String = e.target.result;
            postImageToServer(file.name, file.type, base64String);
          };
    })(file);
        reader.readAsDataURL(file);
    };
});

// -------------------------------------------------------------------------------
function postImageToServer(fileName, fileType, base64String) {
    console.log("postImageToServer:" + base64String) ;
    const badgeNumber = $('#hdnBadgeNumber').val();

    const dataToSend = {
        'badgeNumber' : badgeNumber,
        'file_name' : fileName,
        'file_type' : fileType,
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
    console.log(`processSavePictureResponse`);
    const responseDict = JSON.parse(response);
    console.log(`processSavePictureResponse - responseDict: ${JSON.stringify(responseDict)}`);
    $("#studentImageTmp").attr("src", responseDict.fileBase64);
}



