$(document).ready(function() {
    console.log("Students Details Save Document ready");
})
$("#btnSaveStudentUpdate").click(function() {
    console.log("btnSaveStudentUpdate: Clicked");
    event.preventDefault();
    const formObject = $('#frmStudentDetails');
    let   formData   = $('#frmStudentDetails').serializeArray();

    fetch('save_student_details_api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })
    .then(response   => response.json())
    .then(studentData => ProcessSaveStudentResponse(studentData))
    .catch(error => console.error('Error:', error));

    //save_student_details_api
});

function ProcessSaveStudentResponse(studentData) {
    console.log(`ProcessSaveStudentResponse: ${JSON.stringify(studentData)}`);
}