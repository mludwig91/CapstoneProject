from django.shortcuts import render
from django.conf import settings
from accounts.models import SponsorCompany, UserInformation, Order
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

# Driver view
def shop(request):      
    return render(request, "catalog/shop.html")

def my_catalog(request):
    user = UserInformation.objects.get(user=request.user)
    if user.role_name == 'sponsor':
        company = user.sponsor_company
    else:
        company = user.sponsor_company
    items = CatalogItem.objects.filter(sponsorcatalogitem__in=SponsorCatalogItem.objects.filter(sponsor_company=company)).order_by('pk')
    sponsors = SponsorCatalogItem.objects.filter(catalog_item__in=items).order_by('catalog_item')
    images = CatalogItemImage.objects.filter(catalog_item__in=items).order_by('catalog_item')
    listings = zip(items, sponsors, images)
    return render(request, "catalog/my-catalog.html", context = {'listings' : listings})

# trying to use django-restframework & django-filters 
class Get_Items(generics.ListAPIView):
        queryset = CatalogItem.objects.all()
        serializer_class = ItemSerializer
        filter_backends = [filters.SearchFilter, filters.OrderingFilter]
        ordering_fields = ['last_modified', 'retail_price']
        search_fields = ['item_name', 'item_description']

class SponsorCompanyBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        company = UserInformation.objects.filter(user=self.request.user).sponsor_company
        return queryset.filter(sponsor_company=company)

class Get_Sponsor_Items(generics.ListCreateAPIView):
    
    def get_queryset(self):
        user = UserInformation.objects.get(user=self.request.user)
        if user.role_name == 'sponsor':
            company = user.sponsor_company
        else:
            company = user.sponsor_company
        return SponsorCatalogItem.objects.filter(sponsor_company=company)

    serializer_class = SponsorCatalogItemSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date_added', 'point_value']

def all_items(request):
    if request.method == 'POST':
        add_ID = json.load(request)['ID']
        user = UserInformation.objects.get(user=request.user)
        if user.role_name == 'sponsor':
            company = user.sponsor_company
        else:
            company = user.sponsor_company
        if CatalogItem.objects.filter(api_item_Id=add_ID).exists():
            catalog_item = CatalogItem.objects.filter(api_item_Id=add_ID)[0]
            if SponsorCatalogItem.objects.filter(sponsor_company=company, catalog_item=catalog_item).exists():
                return JsonResponse({'inSponsor' : False})
            else:
                return JsonResponse({'inSponsor' : True})
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

def browse(request):

    if request.method == 'POST':
        add_ID = json.load(request)['ID']

        #add new instance catalog item
        if not CatalogItem.objects.filter(api_item_Id=add_ID).exists():
            url = base_url + '/listings/{}?includes=Images:1&api_key={}'.format(add_ID, key)
            response = requests.request("GET", url)
            search_was_successful = (response.status_code == 200)
            data = response.json()
            listing_data = data['results'][0]
            
            listing = CatalogItem.objects.create(api_item_Id=add_ID)

            
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

            images = listing_data['Images']
            for image in images:
                if image['rank'] == 1:
                    main_image = image['url_170x135']
            CatalogItemImage.objects.create(catalog_item = listing, image_link = main_image)


        user = UserInformation.objects.get(user=request.user)
        if user.role_name == 'sponsor':
            company = user.sponsor_company
        else:
            company = user.sponsor_company
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
        if CatalogItem.objects.all().exists():
            most_recent_update = CatalogItem.objects.order_by('last_updated').first().last_updated
            context = {'last_update' : most_recent_update}
            return render(request, "catalog/browse.html", context=context)
        #else
        return render(request, "catalog/browse.html")


def add_item_to_cart(request, id):
    
    #get user and associate them with an order
    user = UserInformation.objects.get(user=request.user)
    item = CatalogItem.objects.get(api_item_Id=id)
    sponsor_item = SponsorCatalogItem.objects.get(catalog_item=item)
    sponsor = sponsor_item.sponsor_company

    #if item is in the cart already, change qty
    if Order.objects.filter(sponsor_catalog_item = sponsor_item, ordering_driver = user, sponsor = sponsor).exists():
        user.item_count = user.item_count + 1
        sponsor_item.qty_in_cart = sponsor_item.qty_in_cart + 1
        user.save()
        sponsor_item.save()
        return product_page(request,id)
    
    
    #else add item to order list
    order,created = Order.objects.get_or_create(ordering_driver=user, sponsor_catalog_item = sponsor_item, sponsor = sponsor, order_status='inCart')
    sponsor_item.qty_in_cart = 1
    user.item_count = user.item_count + 1
    user.save()
    sponsor_item.save()
    order.save()
    
    return product_page(request,id)

def my_cart(request):
    user = UserInformation.objects.get(user=request.user)
    if Order.objects.filter(ordering_driver=user).exists():
        orders = Order.objects.filter(ordering_driver=user)
        items = []
        order = []
        images = []
        totals_dic = {
            "points": 0,
            "retail": 0
        }
        for obj in orders.iterator():
            items.append(obj.sponsor_catalog_item)
            numitems = obj.sponsor_catalog_item.qty_in_cart
            obj.points_at_order = obj.sponsor_catalog_item.point_value
            obj.retail_at_order =  obj.sponsor_catalog_item.catalog_item.retail_price
            image = CatalogItemImage.objects.get(catalog_item=obj.sponsor_catalog_item.catalog_item)
            obj.save()
            order.append(obj)
            images.append(image)
            for i in range(numitems):
                totals_dic["points"] += obj.points_at_order
                totals_dic["retail"] += obj.retail_at_order                        
        item_list = zip(items, images)
    else:
        item_list = None
        order = None
        totals_dic = None

    return render(request, "catalog/my_cart.html", context = {'item_list': item_list, 'order': order, 'totals_dic': totals_dic})

def remove_item_from_cart(request, id):

    user = UserInformation.objects.get(user=request.user)
    old_item = CatalogItem.objects.get(api_item_Id=id)
    sponsor_item = SponsorCatalogItem.objects.get(catalog_item=old_item)
    order = Order.objects.get(ordering_driver=user, sponsor=sponsor_item.sponsor_company, sponsor_catalog_item=sponsor_item)
    if order.sponsor_catalog_item.qty_in_cart > 1:
        user.item_count = user.item_count-1
        order.sponsor_catalog_item.qty_in_cart = order.sponsor_catalog_item.qty_in_cart - 1
        order.sponsor_catalog_item.save()
        user.save()
    else:
        user.item_count = user.item_count-1
        order.sponsor_catalog_item.qty_in_cart = order.sponsor_catalog_item.qty_in_cart-1
        order.sponsor_catalog_item.delete()
        order.sponsor_catalog_item.save()
        order.delete()
        user.save()
    
    return my_cart(request)

def add_item_from_cart_page(request, id):

    user = UserInformation.objects.get(user=request.user)
    old_item = CatalogItem.objects.get(api_item_Id=id)
    sponsor_item = SponsorCatalogItem.objects.get(catalog_item=old_item)
    order = Order.objects.get(ordering_driver=user, sponsor=sponsor_item.sponsor_company, sponsor_catalog_item=sponsor_item)
    user.item_count = user.item_count + 1
    order.sponsor_catalog_item.qty_in_cart = order.sponsor_catalog_item.qty_in_cart + 1
    user.save()
    order.sponsor_catalog_item.save()

    return my_cart(request)

