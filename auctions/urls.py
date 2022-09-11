from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("login/", logIn, name="login"),
    path("logout/", logOut, name="logout"),
    path("register/", register, name="register"),
    path("listing/<int:pk>/", listing_detail, name="listing-detail"),
    path("add-to-watchlist/<int:pk>/", add_to_watchlist, name="add-to-watchlist"),
    path("remove-from-watchlist/<int:pk>/", remove_from_watchlist, name="remove-from-watchlist")
]