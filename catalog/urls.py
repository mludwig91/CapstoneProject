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
    path('my_cart', views.my_cart, name='my_cart'),
    path('my-catalog', views.my_catalog, name='my-catalog'),
    path('listings', views.listings, name='listings'),
    path('all_items', views.all_items, name='all_items'),
    path('items', views.Get_Items.as_view(), name = 'items'),
    path('sponsor-items', views.Get_Sponsor_Items.as_view(), name = 'sponsor-items'),
    path('browse', views.browse, name = 'browse'),
    path('<int:id>', views.product_page, name = 'product_page'),
    path('add_item/<int:id>/', views.add_item_to_cart, name = 'add_item_to_cart'),
    path('remove_item/<item>/', views.remove_item_from_cart, name = 'remove_item_from_cart')

]