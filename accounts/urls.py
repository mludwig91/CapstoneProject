"""
This module contains our mapping of URL path expressions to Django views for the "accounts" application.
"""
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

# URL namespace for this application.
app_name = 'accounts'

# URL patterns to be matched.
urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='accounts/login.html'), name='logout'),
    path('profile', views.profile, name='profile'),
    path('register', views.register, name='register'),
    path('applied', views.applied, name='applied'),
    path('review_apps', views.review_apps, name='review_apps'),
    path('disable_account', views.disable_account, name='disable_account'),
    path('sponsor_about_page_D', views.sponsor_about_page_D, name='sponsor_about_page_D')
]
