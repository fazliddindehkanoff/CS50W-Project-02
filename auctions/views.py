import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegistrationForm
from . import models, constants

def home(request):

    context = {}
    active_listings = models.Listing.objects.filter(closed=False).all()
    context["active_listings"] = active_listings

    return render(request, "auctions/index.html", context)


def listing_detail(request, pk):
    bid = models.Bid.objects.filter(listing=pk).order_by('-bid').first()  

    context = {}
    context["listing"] = models.Listing.objects.filter(id=pk).first()
    context["bid"] = bid
    context["comments"] = models.Comment.objects.all()
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
def bidding(request, pk):
    bid_amount = request.POST.get("bidding_amount")
    listing = models.Listing.objects.filter(id=pk).first()
    bid_available = models.Bid.objects.filter(user=request.user, listing=listing)
    if bid_available.exists():
        bid_available = bid_available.first()
        bid_available.bid = bid_amount
        bid_available.save()
    else:
        bid = models.Bid()
        bid.bid = bid_amount
        bid.user = request.user
        bid.listing = listing
        bid.save()

    return redirect("listing-detail", pk)

def close_bidding(request, pk):
    listing = models.Listing.objects.filter(id=pk).first()
    bid = models.Bid.objects.filter(listing=listing).order_by("-bid")[0]
    listing.winner = bid.user
    listing.closed = True
    listing.final_price = bid.bid
    listing.save()

    return redirect("listing-detail", pk)

def addComment(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == "POST":
        data = json.load(request)
        pk = data.get("listing_pk")
        comment_text = data.get("comment_text")

        comment = models.Comment()
        comment.user = request.user
        comment.comment = comment_text
        comment.listing = models.Listing.objects.filter(id=pk).first()
        comment.save()

        return HttpResponse("Comment have been added")

def logIn(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
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