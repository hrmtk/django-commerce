from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("add", views.add, name="add"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>", views.entry, name="entry"),
    path("filter/<int:category_id>", views.filter, name="filter"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/say", views.say, name="say"),
    path("<int:listing_id>/watcher", views.watcher, name="watcher"),
    path("<int:listing_id>/close", views.close, name="close"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
