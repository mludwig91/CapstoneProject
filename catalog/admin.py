from django.contrib import admin

from django.contrib import admin
from .models import CatalogItem, CatalogItemImage, SponsorCatalogItem

# Register your models here. 
admin.site.register(CatalogItem)
admin.site.register(CatalogItemImage)
admin.site.register(SponsorCatalogItem)