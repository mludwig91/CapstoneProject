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

function getFilters() {
    var count = 0;
    var filter="";
    if (search !== "") {
        filter = filter + "?search=" + search;
        count++;
    } 
    if (order !== "") {
        if (count > 0) {
            filter = filter + "&";
        }
        else {
            filter = filter + "?";
        }
        filter = filter + "ordering=" + order;
    }
    return filter;
}

function getEtsyFilters() {
    var filter="";
    if (search !== "") {
        filter = filter + "&keywords=" + search;
    }
    return filter;
}

var tab = "";


function getItems() {
    if (tab === "all") {
        getAllItems();
    }
    else if(tab === "manage") {
        getSponsorItems();
    }
    //etsy
    else if (tab === "etsy"){
        getEtsyItems();
    }
}

function getAllItems() {
    $('#item').empty();
    tab = "all";
    var filter = getFilters();
    var endpoint = "/catalog/items" + filter;
    $.ajax({
        url : endpoint,
    })
    .done(function(response) {
        getItemCards(response);
    });
}

function getEtsyItems() {
    $('#item').empty();
    tab = "etsy";
    var etsy_url = "https://openapi.etsy.com/v2"
    var etsy_key = "1a3ofydrsprc5cev28c3vb7l"
    var filter = getEtsyFilters();
    var endpoint = etsy_url + '/listings/active.js?' + 'limit=24&includes=Images:1' + filter + '&api_key=' + etsy_key;
    $.ajax({
        url: endpoint,
        dataType: 'jsonp',
    })
    .done(function(response) {
        var items = response.results;
        getItemCards(items);
    });
}

function getSponsorItems() {
    $('#item').empty();
    tab = "manage";
    var endpoint = "/catalog/sponsor-items";
    $.ajax({
        url : endpoint,
    })
    .done(function(response) {
        getItemCards(response);
    });
}

function getAllSidebar() {
    
}


function getItemCards(items) {
    items.forEach(function(items) {        
        if (tab === "all") {
            var ID = items.api_item_Id;
            var image = items.images[0].image_link;
            var name = items.item_name;
            var price = items.retail_price;
        }
        else if(tab === "manage") {
            var ID = items.catalog_item.api_item_Id;
            var image = items.catalog_item.images[0].image_link;
            var name = items.catalog_item.item_name;
            var price = items.catalog_item.retail_price;
        }
        //etsy
        else {
            var ID = items.listing_id;
            var image = items.Images[0].url_170x135;
            var name = items.title;
            var price = parseFloat(items.price);
        }
        inSponsor(ID);
        $('#item').append(
            '<div class="card m-2 col-sm-4" id="' + ID + '" style="max-width: 20rem;"> ' +
            '<div class="card-body text-center">' +
            '<img class="m-2 mx-auto img-thumbnail" src="' + image + '" width="auto" height="auto" />' +
            '<h5 class="card-title font-weight-bold" data-toggle="tooltip" title="' + name + '">' + name.slice(0,30) + '...</h5>' +
            '<p class="card-text">price: $' + price.toFixed(2) + '</p>' + 
            '<input type="button" class="btn btn-primary change" name="change" id="' + ID + '" value="change" />' +
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
                $('#'+ID+'.card').removeClass("active_card");
                
            }
            else {
                $('#'+ID+".change").val("Remove from Catalog");
                $('#'+ID+'.card').addClass("active_card");
                
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

var search = "";
var order = "";

$(document).ready(function() {
    getAllItems("");  
});

function buttonActive(name) {
    $('.top_group').removeClass("btn-active");
    $('.'+name).addClass("btn-active");
}

$(".all").click(function() {
    buttonActive("all");
    getAllItems();
});

$(".etsy").click(function() {
    buttonActive("etsy");
    getEtsyItems();
});

$(".manage").click(function() {
    buttonActive("manage");
    getSponsorItems();
});

$("#search").click(function() {
    search = $("#searchbar").focus().val();
    getItems();
});


$(".last_mod").click(function() { 
    order = "last_modified";
    getAllItems();
});

$(".last_mod-").click(function() {
    order = "-last_modified";
    getAllItems();
});

$(".price").click(function() { 
    order = "retail_price";
    getAllItems();
});

$(".price-").click(function() {
    order = "-retail_price";
    getAllItems();

});





