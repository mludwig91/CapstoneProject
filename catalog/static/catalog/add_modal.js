function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getProps(body) {
    let props = {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        mode: "same-origin",
    }
    if (body !== null && body !== undefined) {
        props.body = JSON.stringify(body);
    }
    return props;
}

$(document).ready(function() {
    $(".add-modal").click(function() {
        console.log("hello");
        $('#add-modal').modal(show);
    })
});

