"""
This module contains our mapping of URL path expressions to Django views for the "catalog" application.
"""

from django.urls import path
from . import views

# URL namespace for this application.
app_name = 'catalog'

# URL patterns to be matched.
urlpatterns = [
    path('shop', views.shop, name='shop'),
    path('my-catalog', views.my_catalog, name='my-catalog'),
    path('listings', views.listings, name='listings'),
    path('all_items', views.all_items, name='all_items'),
    path('items', views.Get_Items.as_view(), name = 'items'),
    path('sponsor-items', views.Get_Sponsor_Items.as_view(), name = 'sponsor-items')
]