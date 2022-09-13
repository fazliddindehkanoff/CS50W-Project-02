from django.urls import path

from .views import *

urlpatterns = [
    path("login/", logIn, name="login"),
    path("logout/", logOut, name="logout"),
    path("register/", register, name="register"),
]