"""user controller"""
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


# Create your views here.
def logout_user(request):
    """destroy session for requested request"""
    logout(request)
    return HttpResponseRedirect(reverse("base:index"))


def login_user(request):
    """logs a user in into the session"""

    # when method is post
    if request.method == "POST":

        # get username and password
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")
        # check for username and password
        if not username:
            messages.error(request, "Please provide your username.")
        elif not password:
            messages.error(request, "Please provide your password.")
        else:
            # try to authenticate user
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return HttpResponseRedirect(reverse("base:index"))
            messages.error(request, "Invalid username and/or password.")
    # when method is not post
    context = {"title": "login"}
    return render(request, "user/login.html", context)


def register_user(request):
    """register and login a new user"""
    # when method is post
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        if not username:
            messages.error(request, "Please provide your username.")
        elif not password:
            messages.error(request, "Please provide your password.")
        elif not confirmation or confirmation != password:
            messages.error(request, "Please confirm your passowrd.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        else:
            user = User.objects.create(
                username=username, email=username, password=password
            )
            login(request, user)
            messages.success(request, "Registered and logged in successfully.")
            return HttpResponseRedirect(reverse("base:index"))
    context = {"title": "register"}
    return render(request, "user/register.html", context)


class Password:
    """Password object which has several validation methods"""

    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        """returns the string representation of the password"""
        return f"{self.arg}"

    def is_numeric(self):
        """returns true if password is entirely numeric\notherwise false"""
        return self.arg.isdigit()

    def is_strong(self):
        """return true if password has any of !@#$%^&*, otherwise false"""
        return any(char in "!@#$%^&*" for char in self.arg)

    def has_valid_length(self):
        """returns true if length is greater than or equal to 8, otherwise false"""
        return len(self.arg) > 7
