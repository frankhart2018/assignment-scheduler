$(document).ready(function() {

    $("#add-subject").click(function() {
        let data = {
            "subject_name": ["empty"],
        };
        validate_and_post("/add-subject", data, swal_ajax_post);
    });

});