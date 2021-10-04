$(document).ready(function() {

    $("#add-deadline").click(function() {
        let data = {
            "task": ["empty"],
            "subject_name": ["empty"],
            "type": ["empty"],
            "deadline": ["empty"],
        };
        validate_and_post("/add-deadline", data, swal_ajax_post_redirect);
    });

});