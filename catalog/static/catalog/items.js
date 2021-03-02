/*
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
*/
function getItems(filter) {
    var endpoint = "/catalog/items" + filter;
    $.ajax({
        url : endpoint,
    })
    .done(function(response) {
        $('#item').empty();
        getItemCards(response);
    });
}   

function getItemCards(items) {
    items.forEach(function(items) {
        $('#item').append(
            '<div class="card m-2 col-sm-4" style="max-width: 20rem;"> ' +
            '<div class="card-body text-center">' +
            '<img class="m-2 mx-auto img-thumbnail" src="' + items.images[0].image_link + '" width="auto" height="auto" />' +
            '<h5 class="card-title font-weight-bold" data-toggle="tooltip" title="' + items.item_name + '">' + items.item_name.slice(0,30) + '...</h5>' +
            '<p class="card-text">price: $' + items.retail_price + '</p>' +
            '<form id="add" action="" method="POST">' + 
            '<input type="hidden" name="ID" value="' + items.api_item_Id + '"/>' +
            '<input type="submit" name="change" value="add" />' +
            '<input type="submit" name="change" value="Remove" />' +
            '</form>' +
            '</div></div>'
        ); 
    });
}

$(document).ready(function() {
    getItems("");  
});

$(".last_mod").click(function() { 
    getItems("?ordering=date_added");
});

$(".last_mod-").click(function() {
    getItems("?ordering=-date_added");
});
