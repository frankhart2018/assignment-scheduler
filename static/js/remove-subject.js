$(document).ready(function() {

    $("#remove-subject").click(function() {
        let data = {
            "subject_name": ["empty"],
        };
        validate_and_post("/remove-subject", data, swal_ajax_post_redirect);
    });

});