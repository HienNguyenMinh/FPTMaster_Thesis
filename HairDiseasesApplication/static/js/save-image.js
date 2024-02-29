// Show successful message or error message for image saving


$(document).ready(function () {
    $('[id^="saveImageForm"]').submit(function (event) {
        event.preventDefault();

        var formId = $(this).attr('id');
        var successMessageId = formId.replace('saveImageForm', 'successMessage');

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: new FormData(this),
            processData: false,
            contentType: false,
            success: function (data) {
                $('#' + successMessageId).show();
            },
            error: function () {
                alert('Error submitting the form.');
            }
        });
    });
});




