$(document).ready(function() {

    $("#deadlines").DataTable();

    $(".edit-btn").click((e) => {
        let id = e.currentTarget.getAttribute("id");
        id = encodeURIComponent(id);
        window.location.href = `/edit-deadline?task=${id}`;
    });

});