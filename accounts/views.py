"""
This module contains our Django views for the "accounts" application.
"""
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from accounts.forms import UserInformationForm
from accounts.models import UserInformation


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


@login_required(login_url='/accounts/login/')
def profile(request):
    """function profile This function handles the view for the profile page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    # Query for user in the 'User' table
    user = User.objects.get(email=request.user.email)

    # Case 1: The user email exists in our user information table.
    if UserInformation.objects.filter(user=user).exists():
        # Validate that we have a proper user information model
        user_info = UserInformation.objects.get(user=user)
        try:
            user_info.full_clean()

            # Case 1a: The user information model is valid, therefore we can render the profile page.
            request.session.set_expiry(0)
            return render(request, "accounts/profile.html")
        except ValidationError:
            # Case 1b: The user information model is invalid,
            #           we redirect to the register page
            return redirect("/accounts/register")
    # Case 2: The user doesn't have an entry in our user information table,
    #          we redirect to the register page
    else:
        return redirect("/accounts/register")


@login_required(login_url='/accounts/login/')
@csrf_protect
def register(request):
    """function register This function handles the view for the account register page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request depending on whether or not
                      the user is authenticated.
    """
    # Query for user in the 'User' table
    user = User.objects.get(email=request.user.email)

    # Case 1: We have received a POST request with some data
    if request.method == 'POST':
        # Check to see if we are creating a new user information entry or updating an existing one
        if UserInformation.objects.filter(user=user).exists():
            form = UserInformationForm(request.POST, instance=UserInformation.objects.get(user=user))
        else:
            form = UserInformationForm(request.POST)
        # Case 1a: A valid user profile form
        if form.is_valid():
            # Since 'user' is a foreign key, we must store the queried entry from the 'User' table
            user_info = form.save(commit=False)
            user_info.user = user
            user_info.save()
            # Send confirmation email to new user
            msg = EmailMessage(
            'DriveRite Inc',
            '<h2>Thank you for signing up with DriveRite Inc</h2>\
            <h3>A sponsor will review your application and contact \
            you shortly. <br> </br> Sincerely, \
            <br> The DriveRite Team</h3>',
            'DriveRite',
            [user.email])
            msg.content_subtype = "html"
            msg.send()

            # Email sponsor as well

            request.session.set_expiry(0)
            return redirect("/accounts/applied")
        # Case 1b: Not a valid user profile form, render the register page with the current form
        else:
            return render(request, "accounts/register.html", {'form': form})
    # Case 2: We have received something other than a POST request
    else:
        # Case 2a: The user exists in our user information table.
        if UserInformation.objects.filter(user=user).exists():
            form = UserInformationForm(instance=UserInformation.objects.get(user=user),
                                       initial={'user_email': request.user.email})
        # Case 2b: The user email doesn't exist in our user information table.
        else:
            form = UserInformationForm(initial={'user_email': request.user.email, 'first_name': user.first_name})

        request.session.set_expiry(0)
        return render(request, "accounts/register.html", {'form': form})


@login_required(login_url='/accounts/login/')
def applied(request):
    """function logout This function handles the view for the logout page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "accounts/applied.html")

@login_required(login_url='/accounts/login/')
def sponsor_about_page_D(request):
    """function logout This function handles the view for the logout page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    return render(request, "accounts/sponsor_about_page_D.html")


@login_required(login_url='/accounts/login/')
def review_apps(request):
    """function logout This function handles the view for the logout page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """
    current_user = UserInformation.objects.get(user=User.objects.get(email=request.user.email))

    if request.method == 'POST':
        if request.POST.get('approve') is not None:
            print("approving ", request.POST.get('user'))
            pending_user = UserInformation.objects.get(user=User.objects.get(email=request.POST.get('user')))
            pending_user.approving_user = current_user
            pending_user.is_email_verified = True
            pending_user.save()

            # Send Approval email to new user
            msg = EmailMessage(
                'DriveRite Inc',
                '<h2>Your Account Has Been Approved</h2>\
                <h3>After reviewing your application, \
                you have been approved to begin using DriveRite. \
                You may now begin earning rewards!  \
                <br> </br> Sincerely, \
                <br> The DriveRite Team</h3>',
                'DriveRite',
                [pending_user.user.email])
            msg.content_subtype = "html"
            msg.send()

        if request.POST.get('reject') is not None:
            print("rejecting ", request.POST.get('user'))
            pending_user = UserInformation.objects.get(user=User.objects.get(email=request.POST.get('user')))
            pending_user.delete()

            # Send Reject email to new user
            msg = EmailMessage(
                'DriveRite Inc',
                '<h2>Your Account Has Been Rejected</h2>\
                <h3>After reviewing your application, \
                unfortunately you have been denied. \
                Please reach out if you think there \
                has been a mistake!  \
                <br> </br> Sincerely, \
                <br> The DriveRite Team</h3>',
                'DriveRite',
                [pending_user.user.email])
            msg.content_subtype = "html"
            msg.send()

    open_apps = UserInformation.objects.filter(sponsor_company=current_user.sponsor_company).filter(is_email_verified=False).all()
    return render(request, "accounts/review_apps.html", {'open_apps': open_apps})


@login_required(login_url='/accounts/login/')
def disable_account(request):

    if request.method == 'POST':
        #Get user instance
        user = request.user
        #If post request includes "Disable", change is_active flag
        if request.POST.get("Disable"):
            user.is_active = False
            user.save()
            messages.success(request, 'Profile successfully disabled')
        #Otherwise redirect back to profile
        else:
            return redirect("/accounts/profile")

    return render(request, "accounts/disable_account.html")