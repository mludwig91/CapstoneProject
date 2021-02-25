from rest_framework import serializers
from accounts.models import CatalogItem, SponsorCatalogItem, CatalogItemImage, SponsorCompany, UserInformation


class CatalogItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogItemImage
        fields = ['image_link']


class ItemSerializer(serializers.ModelSerializer):
    #sponsorcatalogitem_set = SponsorCatalogItemSerializer(many=True,read_only=True)
    images = CatalogItemImageSerializer(many=True,read_only=True)
    
    class Meta:
        model = CatalogItem
        fields = ['item_name', 'item_description', 'retail_price', 'is_available', 'last_update', 'api_item_Id', 'images']

class SponsorCatalogItemSerializer(serializers.ModelSerializer):
    sponsor_company = serializers.SlugRelatedField(read_only=True, slug_field='company_name')
    catalog_item = ItemSerializer(read_only = True)

    class Meta:
        model = SponsorCatalogItem
        fields = ['sponsor_company', 'point_value', 'last_update', 'is_available_to_drivers', 'catalog_item']

        
