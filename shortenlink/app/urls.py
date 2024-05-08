"""urls for shortenlink app"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("shorten", views.shorten, name="shorten"),
    path("urls", views.urls, name="urls"),
    path("redirect/<str:short_url>", views.redirect, name="redirect"),
]
