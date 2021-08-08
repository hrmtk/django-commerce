from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category
from .forms import NewListingForm, CommentForm

from decimal import Decimal


def index(request):
    lists = Listing.objects.filter(active=True)
    bids = Bid.objects.all()
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "lists": lists,
        "categories": categories
    })
        

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


def filter(request, category_id):
    categories = Category.objects.all()
    item_category = Category.objects.get(pk=category_id)
    lists = Listing.objects.filter(active=True, category=item_category)
    bids = Bid.objects.all()
    return render(request, "auctions/filter.html", {
        "lists": lists,
        "bids": bids,
        "categories": categories,
        "item_category": item_category
    })


def entry(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing=listing)
    bidders_count = Bid.objects.filter(listing=listing).count()
    form1 = CommentForm()
    message = None

    # If user is winner, the message say so
    if request.user.is_authenticated:
        user_bids = Bid.objects.filter(listing=listing, bidders=request.user, bids=listing.current_price).count()
        if not listing.active and user_bids:
            message = "Congratulations! You Won!!" 

    return render(request, "auctions/entry.html", {
        "listing": listing,
        "comments": comments,
        "bidders_count": bidders_count,
        "non_watchers": User.objects.exclude(watchlists=listing).all(),
        "form1": form1,
        "message": message
    })


@login_required
def add(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.current_price = obj.starting_bid
            obj.active = True
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = NewListingForm()
        return render(request, "auctions/add.html", {
            "form": form
        })


@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        new_bid = Decimal(request.POST.get("price"))

        if listing.current_price > new_bid:
            return HttpResponseRedirect(reverse("entry", args=(listing.id,)))
        else:
            listing.current_price = new_bid
            listing.save()
            b = Bid(listing=listing, bids=new_bid)
            b.save()
            b.bidders.add(request.user)
            return HttpResponseRedirect(reverse("entry", args=(listing.id,)))


@login_required
def say(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.listing = listing
            form.save()
            return HttpResponseRedirect(reverse("entry", args=(listing.id,)))


@login_required
def watcher(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        non_watchers =  User.objects.exclude(watchlists=listing).all()
        user = User.objects.get(username=request.user.username)
        if user in non_watchers:
            user.watchlists.add(listing)
        else:
            user.watchlists.remove(listing)
        return HttpResponseRedirect(reverse("entry", args=(listing.id,)))


@login_required
def close(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("entry", args=(listing.id, )))


@login_required
def mypage(request):
    listing = Listing.objects.filter(owner=request.user)
    return render(request, "auctions/mypage.html", {
        "listing": listing
    })


@login_required
def watchlist(request):
    user = User.objects.get(username=request.user.username)
    lists = user.watchlists.all()
    bids = Bid.objects.all()
    categories = Category.objects.all()
    return render(request, "auctions/watchlist.html", {
        "lists": lists,
        "bids": bids,
        "categories": categories
    })