from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("login/", logIn, name="login"),
    path("logout/", logOut, name="logout"),
    path("register/", register, name="register"),
    path("listing/<int:pk>/", listing_detail, name="listing-detail")
]