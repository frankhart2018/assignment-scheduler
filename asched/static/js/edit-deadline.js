$(document).ready(function() {

    $("#edit-deadline").click(function() {
        let data = {
            "task": ["empty"],
            "subject_name": ["empty"],
            "type": ["empty"],
            "deadline": ["empty"],
            "status": ["empty"],
        };
        
        validate_and_post("/edit-deadline", data, swal_ajax_post_redirect);
    });

});