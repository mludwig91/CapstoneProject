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
        inSponsor(items.api_item_Id)
        $('#item').append(
            '<div class="card m-2 col-sm-4" id="' + items.api_item_Id + '" style="max-width: 20rem;"> ' +
            '<div class="card-body text-center">' +
            '<img class="m-2 mx-auto img-thumbnail" src="' + items.images[0].image_link + '" width="auto" height="auto" />' +
            '<h5 class="card-title font-weight-bold" data-toggle="tooltip" title="' + items.item_name + '">' + items.item_name.slice(0,30) + '...</h5>' +
            '<p class="card-text">price: $' + items.retail_price.toFixed(2) + '</p>' + 
            '<input type="button" class="btn change" name="change" id="' + items.api_item_Id + '" value="change" />' +
            '</div></div>'
        ); 
    });

    function inSponsor(ID) {
        let body = {
            "ID": ID
        };
        var props = getProps(body);
        fetch('/catalog/all_items', props)
        .then(function(response) {
            return response.json();
        })
        .then(function(response) { 
            if (Boolean(response.inSponsor)) {
                $('#'+ID+'.change').val("Add to Catalog");
                $('#'+ID+'.card').removeClass("active");
                
            }
            else {
                $('#'+ID+".change").val("Remove from Catalog");
                $('#'+ID+'.card').addClass("active");
                
            }
        })
    }
    $('.change').click(function(e) {
        e.preventDefault();
        var ID = this.id;
        let body = {
            "ID": ID
        };
        var props = getProps(body);
        fetch('/catalog/browse', props)
        .then(function(response) {
            return response;
        })
        .then(function() {
            inSponsor(ID);
        })
    })
}

$(document).ready(function() {
    getItems("");  
});

$(".last_mod").click(function() { 
    getItems("?ordering=last_modified");
});

$(".last_mod-").click(function() {
    getItems("?ordering=-last_modified");
});

$(".price").click(function() { 
    getItems("?ordering=retail_price");
});

$(".price-").click(function() {
    getItems("?ordering=-retail_price");
});