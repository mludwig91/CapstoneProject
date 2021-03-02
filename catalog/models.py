from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.db.models.constraints import UniqueConstraint
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import DateTimeField
import datetime

#import accounts.models

class CatalogItem(models.Model):
    """
    Model of a particular catalog item.
    """
    item_name = models.CharField("Item Name", max_length=256, validators=[MinLengthValidator(1)], null=True)
    item_description = models.TextField("Item Description", validators=[MinLengthValidator(1)], null=True)
    retail_price = models.FloatField("Retail Price (MSRP)", null=True, validators=[MinValueValidator(0.01)])
    is_available = models.BooleanField("Item is Available From Retail", default=False)
    last_modified = models.IntegerField("Epoch time of Last Update to Item", validators=[MinValueValidator(1)], null=True)
    api_item_Id = models.CharField("API Link/Identifier", max_length=256, validators=[MinLengthValidator(1)], unique=True)


class CatalogItemImage(models.Model):
    """
    Model of a particular image belonging to a particular catalog item.
    """
    catalog_item = models.ForeignKey(CatalogItem, related_name='images', on_delete=CASCADE)
    image_link = models.URLField("Static Image Link")


class SponsorCatalogItem(models.Model):
    """
    Model of a sponsor's particular catalog item, which may be made available to their drivers.
    """
    catalog_item = models.ForeignKey(CatalogItem, on_delete=CASCADE)
    sponsor_company = models.ForeignKey("accounts.SponsorCompany", on_delete=CASCADE)
    point_value = models.IntegerField("Driver Point Value", validators=[MinValueValidator(1)])
    date_added = models.DateTimeField("DateTime of Last Update to Item", default=datetime.datetime.utcnow)
    is_available_to_drivers = models.BooleanField("Is Item Available For Driver Redemption", default=False)