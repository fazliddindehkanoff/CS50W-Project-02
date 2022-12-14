from django.urls import path

from .views import *

urlpatterns = [
    #listing
    path("", home, name="home"),
    path("listing/<int:pk>/", listing_detail, name="listing-detail"),
    path("create-listing/", create_listing, name="create-listing"),
    #watchlist
    path("my-watchlist/", watchList, name="my-watchlist"),
    path("add-to-watchlist/<int:pk>/", add_to_watchlist, name="add-to-watchlist"),
    path("remove-from-watchlist/<int:pk>/", remove_from_watchlist, name="remove-from-watchlist"),
    #bidding
    path("add-bidding/<int:pk>/", bidding, name="add-bidding"),
    path("close-bidding/<int:pk>/", close_bidding, name="close-bidding"),
    #comment
    path("add-comment/", addComment, name="add-comment"),
    #categories
    path("categories/", categories, name="categories")
]