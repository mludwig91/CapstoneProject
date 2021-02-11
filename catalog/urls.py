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
]
