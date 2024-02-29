$(document).ready(function () {
    $('#saveAllBtn').click(function (event) {
        event.preventDefault();  // Prevent the default form submission

        var formDataArray = [];

        // Loop through all saveImageForm forms
        $('[id^="saveImageForm"]').each(function () {
            var formData = {
                'file-path': $(this).find('input[name="file-path"]').val(),
                'conclusion-input': $(this).find('input[name="conclusion-input"]').val(),
                'patient-ID': $(this).find('input[name="patient-ID"]').val()
            };
            formDataArray.push(formData);
        });

        // Send the data to the server using AJAX
        $.ajax({
            url: '/saveAll',
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(formDataArray),
            dataType: 'json',
            success: function (data) {
                // Handle success, if needed
                console.log('Save All successful!');
                $('#successAllMessage').show();
            },
            error: function () {
                // Handle error, if needed
                alert('Error saving all images.');
            }
        });
    });
});
