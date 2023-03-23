from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    listing = Listing.objects.filter(active = True)
    return render(request, "auctions/index.html", {
        "listings": listing
    })

def categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        print(categories)
        return render(request, "auctions/categories.html", {
            "categories": categories
        })
    else:
        cat = request.POST["cat"]
        category = Category.objects.get(name = cat)
        listings = Listing.objects.filter(active = True, category=category)
        print(type(cat), type(category), listings)
        return render(request, "auctions/categories.html", {
            "cat": cat,
            "listings":listings
        })


def item(request, item_id, key=None):
    listing = Listing.objects.get(pk = item_id)
    user = request.user
    comments = Comment.objects.filter(listing = listing)
    owner = request.user.username == listing.owner.username
    if user in listing.watchlist.all():
        watchlist = True
    else:
        watchlist = False
    item = Listing.objects.get(id = item_id)
    return render(request, "auctions/item.html", {
        "list": item,
        "watchlist": watchlist,
        "comments": comments,
        "success": key,
        "owner": owner,
    })

def close(request, item_id):
    listing = Listing.objects.get(pk = item_id)
    listing.active = False
    listing.save()
    key = 3
    return HttpResponseRedirect(reverse("productSuccess", args = (item_id, key)))

def addcomment(request, item_id):
    product = Listing.objects.get(pk = item_id)
    poster = request.user
    post = request.POST['body']
    # print(product, poster, post)
    newpost = Comment(
        body = post,
        owner = poster,
        listing = product,
    )

    newpost.save()

    return HttpResponseRedirect(reverse("product", args = (item_id, )))


def watchlist(request):

    listings = request.user.userWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def remove(request, id):
    listing = Listing.objects.get(pk = id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("product", args = (id, )))

def add(request, id):
    listing = Listing.objects.get(pk = id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("product", args = (id, )))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        # get data from form
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["imageurl"]
        # active = request.POST["active"]
        category = Category.objects.get(name = request.POST["category"])

        # get user identity
        user = request.user

        # create a new bid object
        bid = Bid(bid = float(price), owner = user)
        bid.save()

        # create a new object
        ob = Listing(title=title, description = description, price = bid, image = image, category = category, owner = user)

        # insert object into data
        ob.save()
        # reidirect to index
        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Category.objects.all()
        return render(request, "auctions/createlisting.html", {
            "category": categories
        })


def bid(request, item_id):
    product = Listing.objects.get(pk = item_id)
    poster = request.user
    bid = request.POST['body']

    if float(bid) > float(product.price.bid):
        print(product, poster, bid)
        newpost = Bid(bid = bid, owner = poster)
        newpost.save()
        product.price = newpost
        product.save()
        key = 1
        return HttpResponseRedirect(reverse("productSuccess", args = (item_id, key)))
    else:
        key = 2
        return HttpResponseRedirect(reverse("productSuccess", args = (item_id, key)))
