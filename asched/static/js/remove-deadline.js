$(document).ready(function() {

    $("#remove-deadline").click(function() {
        let data = {
            "task": ["empty"],
        };
        validate_and_post("/remove-deadline", data, swal_ajax_post_redirect);
    });

});