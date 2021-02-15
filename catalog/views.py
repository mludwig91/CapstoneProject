from django.shortcuts import render
from django.conf import settings
from accounts.models import CatalogItem
import json
import requests

# Create your views here.


base_url = settings.ETSY_BASE_URL
key = settings.ETSY_API_KEY
'''
def shop(request):
    url = base_url + '/listings/active/?limit=10&api_key={}'.format(key)
    response = requests.request("GET", url)
    search_was_successful = (response.status_code == 200)
    data = response.json()
    listings = data['results']
    for listing in listings:
            url = base_url + '/listings/{}/images?api_key={}'.format(listing['listing_id'], key)
            response = requests.request("GET", url)
            search_was_successful = (response.status_code == 200)
            image_data = response.json()
            images = image_data['results']
            for image in images:
                if image['rank'] == 1:
                    listing['main_image'] = image['url_170x135']
    return render(request, "catalog/shop.html", {'listings' : listings})
'''
# return a listing off of its Listing_ID 
# check to see if the Listing_ID has been modified
def shop(request):

    # get all databse instances for items
    listings = CatalogItem.objects.all() 
    
    # update all listings
    for listing in listings:
        # check if the modfied time has been changed 
        # need to import better epoch time library
        # use listing_id to get listings.
        url = '/listings/{}?api_key={}'.format(listing.listing_id, key)
        response = requests.request("GET", url)
        search_was_successful = (response.status_code == 200)
        data = response.json()
        listing_data = data['results']

        listing.item_name = listing_data['title']
        listing.item_description = listing_data['description']
        # ignore foreign currency for now
        listing.retail_price = listing_data['price']
        if listing_data['state'] is "active":
            listing.is_available = True
        else:
            listing.is_available = False

        listing.save()

    return render(request, "catalog/shop.html")
    

        
