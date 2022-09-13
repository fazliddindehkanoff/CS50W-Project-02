from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from .forms import LoginForm, RegistrationForm

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
