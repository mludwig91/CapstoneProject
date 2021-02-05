"""
This module registers the models we created for the "accounts" application. After registering
the model, the data will be accessible through Django's admin functionality.
"""

# Register your models here.
from django.contrib import admin
from .models import UserInformation


class UserInformationAdmin(admin.ModelAdmin):
    """
    This class contains rendering details for the UserInformation table
    """
    model = UserInformation
    list_display = ('get_user_email', 'first_name')     # Fields to be shown initially


# Register your models here.
admin.site.register(UserInformation, UserInformationAdmin)