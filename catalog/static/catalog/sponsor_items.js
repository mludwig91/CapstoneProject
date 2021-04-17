function getItems(filter) {
    var endpoint = "/catalog/sponsor-items" + filter;
    $.ajax({
        url : endpoint,
    })
    .done(function(response) {
        $('#item').empty();
        getSponsorItemCards(response);
    });
}   

function getSponsorItemCards(items) {
    items.forEach(function(items) {
        $('#item').append(
            '<div class="card m-2 col-sm-4" style="max-width: 20rem;"> ' +
            '<div class="card-body text-center">' +
            '<img class="m-2 mx-auto img-thumbnail" src="' + items.catalog_item.images[0].image_link + '" width="auto" height="auto" />' +
            '<h5 class="card-title font-weight-bold" data-toggle="tooltip" title="' + items.catalog_item.item_name + '">' + items.catalog_item.item_name.slice(0,30) + '...</h5>' +
            '<p class="card-text">points: ' + items.point_value + '</p>' +
            '<a href="/catalog/product-page/' + items.catalog_item.api_item_Id + ' " class="btn btn-primary px-auto">See full details</a>' +
            '</div></div>'
        ); 
    });
}

$(document).ready(function() {
    getItems("");  
});

$(".date_added").click(function() { 
    getItems("?ordering=date_added");
});

$(".date_added-").click(function() {
    getItems("?ordering=-date_added");
});

$(".points").click(function() {
    getItems("?ordering=point_value");
});

$(".points-").click(function() {
    getItems("?ordering=-point_value");
});