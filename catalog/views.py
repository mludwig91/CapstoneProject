from django.shortcuts import render
from django.conf import settings
import json
import requests

# Create your views here.


base_url = settings.ETSY_BASE_URL
key = settings.ETSY_API_KEY

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
