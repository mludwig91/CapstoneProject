"""
This module contains our Django views for the "accounts" application.
"""
from django.shortcuts import render, redirect


def login(request):
    """function login This function handles the view for the login page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "accounts/login.html")


def logout(request):
    """function logout This function handles the view for the logout page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return redirect("/")


def profile(request):
    """function logout This function handles the view for the profile page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return redirect(request, "accounts/profile.html")
