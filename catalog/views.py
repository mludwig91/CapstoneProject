from django.shortcuts import render
from django.conf import settings
from accounts.models import SponsorCompany, UserInformation
from catalog.models import CatalogItem, SponsorCatalogItem, CatalogItemImage
from catalog.serializers import ItemSerializer, SponsorCatalogItemSerializer
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import generics
from django.utils import timezone
import json
import requests

# Create your views here.


base_url = settings.ETSY_BASE_URL
key = settings.ETSY_API_KEY


def shop(request):

    if request.method == 'POST':
        add_ID = json.load(request)['ID']
        user = UserInformation.objects.get(user=request.user)
        if user.role_name == 'sponsor':
            company = user.sponsor_company.all()[0]
        else:
            company = user.sponsor_company.all()[0]
        catalog_item = CatalogItem.objects.filter(api_item_Id=add_ID)[0]

        # check not already in sponsor
        if not SponsorCatalogItem.objects.filter(sponsor_company=company, catalog_item=catalog_item).exists():
            # calculate points
            ratio = company.company_point_ratio 
            cents = (int)(catalog_item.retail_price * 100)
            points = (int)(cents/ratio)

            # create new sponspor item and add to database
            new_sponsor_item = SponsorCatalogItem(sponsor_company=company, catalog_item=catalog_item, point_value=points, is_available_to_drivers=True)
            new_sponsor_item.save()

        else:
            SponsorCatalogItem.objects.filter(sponsor_company=company, catalog_item=catalog_item).delete()
            
        return JsonResponse({'success' : 'sucess'})

    else:
        most_recent_update = CatalogItem.objects.order_by('last_updated').first().last_updated
        context = {'last_update' : most_recent_update}
        
    
    return render(request, "catalog/shop.html", context=context)
    
    
def my_catalog(request):
    user = UserInformation.objects.get(user=request.user)
    if user.role_name == 'sponsor':
        company = user.sponsor_company.all()[0]
    else:
        company = user.sponsor_company.all()[0]
    items = CatalogItem.objects.filter(sponsorcatalogitem__in=SponsorCatalogItem.objects.filter(sponsor_company=company)).order_by('pk')
    sponsors = SponsorCatalogItem.objects.filter(catalog_item__in=items).order_by('catalog_item')
    images = CatalogItemImage.objects.filter(catalog_item__in=items).order_by('catalog_item')
    listings = zip(items, sponsors, images)
    return render(request, "catalog/my-catalog.html", context = {'listings' : listings})

# trying to use django-restframework & django-filters 
class Get_Items(generics.ListAPIView):
        queryset = CatalogItem.objects.all()
        serializer_class = ItemSerializer
        filter_backends = [filters.OrderingFilter]
        ordering_fields = ['last_modified', 'retail_price']


class SponsorCompanyBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        company = UserInformation.objects.filter(user=self.request.user).sponsor_company
        return queryset.filter(sponsor_company=company)


class Get_Sponsor_Items(generics.ListCreateAPIView):
    queryset = SponsorCatalogItem.objects.all()
    serializer_class = SponsorCatalogItemSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_added', 'point_value']


def all_items(request):
    if request.method == 'POST':
        add_ID = json.load(request)['ID']
        user = UserInformation.objects.get(user=request.user)
        if user.role_name == 'sponsor':
            company = user.sponsor_company.all()[0]
        else:
            company = user.sponsor_company.all()[0]
        catalog_item = CatalogItem.objects.filter(api_item_Id=add_ID)[0]
        if SponsorCatalogItem.objects.filter(sponsor_company=company, catalog_item=catalog_item).exists():
            return JsonResponse({'inSponsor' : False})
        else:
            return JsonResponse({'inSponsor' : True})

def listings(request):
    
    # get all database instances for items and update all listings
    for listing in CatalogItem.objects.all():
        url = base_url + '/listings/{}?api_key={}'.format(listing.api_item_Id, key)
        response = requests.request("GET", url)
        search_was_successful = (response.status_code == 200)
        data = response.json()
        listing_data = data['results'][0]

        listing.last_updated = timezone.now()
        listing.last_modified = listing_data['last_modified_tsz']
        # check if the modfied time has been changed 
        listing.item_name = listing_data['title']
        listing.item_description = listing_data['description']
        # ignore foreign currency for now
        listing.retail_price = float(listing_data['price'])
        if listing_data['state'] == "active":
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

    return render(request, "catalog/listings.html")

def product_page(request, id):
    user = UserInformation.objects.get(user=request.user)
    company = user.sponsor_company
    items = CatalogItem.objects.filter(api_item_Id = id)
    sponsors = SponsorCatalogItem.objects.filter(catalog_item__in=items)
    images = CatalogItemImage.objects.filter(catalog_item__in=items)
    listings = zip(items, sponsors, images)
    return render(request, "catalog/product_page.html", context = {'listings' : listings})


