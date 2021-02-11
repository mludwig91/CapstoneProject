from django.shortcuts import render
import requests

# Create your views here.


def shop(request):

    return render(request, "catalog/shop.html")

'''
def shop(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
    response = requests.get('https://openapi.etsy.com/v2/listings/active?api_key=/%s' % ip_address)
    listings = response.json()
'''