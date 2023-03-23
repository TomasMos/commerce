from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
            return f"{self.username}"

class Listing(models.Model):
    title = models.CharField(max_length = 64)
    description = models.CharField(max_length = 1000)
    price = models.ForeignKey('Bid', on_delete = models.CASCADE, related_name = "bidprice")
    active = models.BooleanField(default = True)
    image = models.CharField(max_length = 1000)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user")
    category = models.ForeignKey('Category', on_delete = models.CASCADE, related_name = "category")
    watchlist = models.ManyToManyField(User, related_name = "userWatchlist")

    def __str__(self):
        return f"{self.title}"

class Category(models.Model):
    name = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.name}"

class Comment(models.Model):
    body = models.CharField(max_length = 2000)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "Listing_comment")
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "owner_comment")

    def __str__(self):
        return f"{self.owner} commented on {self.listing}"

class Bid(models.Model):
    bid = models.FloatField(default = 0)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user_bid")

    def __str__(self):
        return f"{self.bid}"

