$(document).ready(function() {

    $.ajax({
        url: '/catalog/items',
    })
    .done(function(response) {
        renderItems(response);
    });

    function renderItems(items) {
        var $itemContainer = $('#item');
        items.forEach(
        $itemContainer.append(createCard(item))
        );
    }


    function createCard(item) {
        card = sdf
    }    
  
  /*      '<div class="card" style = "width: 18rem;">' +
            '<img src="' + item.images[0].image_link + '", alt="Card image cap">' +
            '<div>' + item.item_name + '</div>' + 
            '</div>'
        )
*/
    

});


    



/*
function getItems() {
    $.getJSON(URL,{},showItems)
}
function getItem() {
    $.getJSON(URL+$("#id").val())
    .done(showItem)
}

function showItem(item) {
    $("#item_name").val(item.item_name)
}
*/



