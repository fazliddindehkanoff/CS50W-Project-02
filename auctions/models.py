from django.db import models
from django.contrib.auth.models import AbstractUser

from .constants import CATEGORIES

class User(AbstractUser):
    pass

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    category = models.IntegerField(choices=CATEGORIES, null=True)
    link = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    final_price = models.IntegerField(default=0)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="winner")

    def __str__(self):
        return self.title

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.user} - {self.listing} - {self.bid}$"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.listing}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.listing}"

