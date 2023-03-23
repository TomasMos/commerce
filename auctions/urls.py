from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name= "login"),
    path("logout/", views.logout_view, name= "logout"),
    path("register/", views.register, name= "register"),
    path("create/", views.create_listing, name = "createlisting"),
    path("categories/", views.categories, name= "categories"),
    path("products/<int:item_id>/", views.item, name = "product" ),
    path("products/<int:item_id>/<int:key>", views.item, name = "productSuccess"),
    path("remove/<int:id>", views.remove, name = "remove"),
    path("add/<int:id>", views.add, name = "add"),
    path("watchlist/", views.watchlist, name = "watchlist"),
    path("addcomment/<int:item_id>", views.addcomment, name = "addcomment"),
    path("bid/<int:item_id>", views.bid, name = "bid"),
    path("close/<int:item_id>", views.close, name = "close"),
]
