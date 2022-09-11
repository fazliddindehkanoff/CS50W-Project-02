from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .forms import LoginForm, RegistrationForm
from . import models, constants

def home(request):

    context = {}
    active_listings = models.Listing.objects.filter(closed=False).all()
    context["active_listings"] = active_listings

    return render(request, "auctions/index.html", context)


def listing_detail(request, pk):

    context = {}
    context["listing"] = models.Listing.objects.filter(id=pk).first()
    context["bid"] = models.Bid.objects.filter(listing=pk).aggregate(Max("bid"))
    context["in_watchlist"] = models.Watchlist.objects.filter(user=request.user, listing=pk).exists()

    return render(request, "auctions/listing-detail.html", context)

@login_required(login_url="login")
def add_to_watchlist(request, pk):
    watchlist = models.Watchlist()
    watchlist.user = request.user
    watchlist.listing = models.Listing.objects.filter(id=pk).first()
    watchlist.save()

    return redirect("listing-detail", pk)

@login_required(login_url="login")
def remove_from_watchlist(request, pk):
    models.Watchlist.objects.get(user=request.user, listing_id=pk).delete()
    return redirect("listing-detail", pk)

@login_required(login_url="login")
def bidding(request, pk, bid_amount):
    bid = models.Bid()
    

def logIn(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            print(user, username, password)
            if user is not None:
                login(request, user)
                messages.success(request, message="Logged in successfully")
                return redirect("home")
            else:
                messages.error(request, "Username or Password is not correct")

    return render(request, "auctions/login.html", {"form": form})

@login_required(login_url="login")
def logOut(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("home")

def register(request):
    form = RegistrationForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            return redirect("login")

    return render(request, "auctions/register.html", {"form": form})