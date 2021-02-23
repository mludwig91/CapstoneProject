from django.shortcuts import render
from django.conf import settings
from accounts.models import CatalogItem, CatalogItemImage
import json
import requests

# Create your views here.


base_url = settings.ETSY_BASE_URL
key = settings.ETSY_API_KEY


def shop(request, *args, **kwargs):
    # get all database instances for items and update all listings
    for listing in CatalogItem.objects.all() :
        url = base_url + '/listings/{}?api_key={}'.format(listing.api_item_Id, key)
        response = requests.request("GET", url)
        search_was_successful = (response.status_code == 200)
        data = response.json()
        listing_data = data['results'][0]

        # check if the modfied time has been changed 
        listing.item_name = listing_data['title']
        listing.item_description = listing_data['description']
        # ignore foreign currency for now
        listing.retail_price = float(listing_data['price'])
        if listing_data['state'] is "active":
            listing.is_available = True
        else:
            listing.is_available = False
        listing.save()

        # create new catalog item image instance if one doesnt exist
        if not CatalogItemImage.objects.filter(catalog_item = listing).exists():
            url = base_url + '/listings/{}/images?api_key={}'.format(listing.api_item_Id, key)
            response = requests.request("GET", url)
            search_was_successful = (response.status_code == 200)
            image_data = response.json()
            images = image_data['results']
            for image in images:
                if image['rank'] == 1:
                    main_image = image['url_170x135']
            CatalogItemImage.objects.create(catalog_item = listing, image_link = main_image)

    # gather objects to be used in html 
    items = CatalogItem.objects.all()
    images = CatalogItemImage.objects.all()
    listings = zip(items, images)

    return render(request, "catalog/shop.html", context = {'listings' : listings})
    
# need some kind of additional inheritance so CatalogItemImage can be accessed through CatalogItem