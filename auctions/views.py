import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . import models, constants, forms

def home(request):
    context = {}
    category = request.GET.get("category", None)

    if category:
        active_listings = models.Listing.objects.filter(closed=False, category=category)
    else:
        active_listings = models.Listing.objects.filter(closed=False).all()

    context["active_listings"] = active_listings

    return render(request, "auctions/index.html", context)

def listing_detail(request, pk):
    bid = models.Bid.objects.filter(listing=pk).order_by('-bid').first()  

    context = {}
    context["listing"] = models.Listing.objects.filter(id=pk).first()
    context["bid"] = bid
    context["comments"] = models.Comment.objects.all()
    try:
        context["in_watchlist"] = models.Watchlist.objects.filter(user=request.user, listing=pk).exists()
    except TypeError:
        context["in_watchlist"] = False

    return render(request, "auctions/listing-detail.html", context)

@login_required(login_url="login")
def watchList(request):
    context = {}
    watchlist = models.Watchlist.objects.filter(user=request.user).all()
    context["watchlists"] = watchlist

    return render(request, "auctions/watchlist.html", context)

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

@login_required(login_url="login")
def close_bidding(request, pk):
    listing = models.Listing.objects.filter(id=pk).first()
    bid = models.Bid.objects.filter(listing=listing).order_by("-bid")[0]
    listing.winner = bid.user
    listing.closed = True
    listing.final_price = bid.bid
    listing.save()

    return redirect("listing-detail", pk)

@login_required(login_url="login")
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

@login_required(login_url="login")
def categories(request):

    context = {}
    context["categories"] = constants.CATEGORIES

    return render(request, "auctions/categories.html", context)

@login_required(login_url="login")
def create_listing(request):
    form = forms.ListingForm(user=request.user)
    context = {}

    if request.method == "POST":
        form = forms.ListingForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")


    context["form"] = form

    return render(request, "auctions/create-listing.html", context)