from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from urllib.parse import urlparse

from . import service
from .shortenlink.exception import ShortenURLCreationError, ShortenURLRetrievalError


# Create your views here.
@login_required(login_url="/login")
def index(request: HttpRequest) -> HttpResponse:
    """Index page"""
    return render(request, "shorten.html", {"username": request.user.username})


@login_required(login_url="/login")
@api_view(["GET", "POST"])
def shorten(request: HttpRequest) -> HttpResponse:
    """Shorten page"""
    if request.method == "POST":
        return shorten_post(request)
    return render(request, "shorten.html", {"username": request.user.username})


def shorten_post(request: HttpRequest) -> HttpResponse:
    """Shorten a URL"""
    # get the URL from the request
    url = request.POST.get("url")
    if not url:
        messages.error(request, "URL is required")
        return render(request, "shorten.html", {"username": request.user.username})
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        messages.error(request, "Invalid URL")
        return render(request, "shorten.html", {"username": request.user.username})
    # shorten the URL
    try:
        short_url = service.shorten_url(url)
    except ShortenURLCreationError:
        # return 400 if failed to create
        return HttpResponse(status=400, reason="Failed to create shorten URL")
    except ShortenURLRetrievalError:
        # return 500 if failed to retrieve
        return HttpResponse(
            status=500, reason="Shorten URL already exists, but failed to retrieve"
        )
    absolute_short_url = request.build_absolute_uri("redirect/" + short_url)

    # return the short URL
    return render(
        request,
        "shorten_succeed.html",
        {"short_url": absolute_short_url, "username": request.user.username},
    )


def redirect(request: HttpRequest, short_url: str) -> HttpResponse:
    """Redirect to the original URL"""
    # short_url = request.GET.get("short_url")
    if not short_url:
        return HttpResponse(status=400, reason="Short URL is required")
    try:
        ip_address = request.META.get("REMOTE_ADDR")
        print(ip_address)
        service.record_activity(short_url, service.UserInfo(ip_address))
        url = service.retrieve_url(short_url)
    except Exception as e:
        print(e)
        # return HttpResponse(status=404, reason="Short URL not found")
        raise
    return HttpResponse(status=302, reason="Redirecting", headers={"Location": url})


@login_required(login_url="/login")
def urls(request: HttpRequest) -> HttpResponse:
    """URLs page"""
    page = request.GET.get("page", 1)
    try:
        page = max(1, int(page))
    except ValueError:
        page = 1

    mapping_num, mappings = service.display_urls()

    short_url = request.GET.get("short_url")
    short_urls = [mp["short_url"] for mp in mappings]
    if not short_url or short_url not in short_urls:
        short_url = mappings[0]["short_url"]

    url, page, tracking_num, trackings = service.display_records(short_url, page=page)
    absolute_short_url = request.build_absolute_uri("redirect/" + short_url)
    return render(
        request,
        "urls.html",
        {
            "mapping_num": mapping_num,
            "mappings": mappings,
            "url": url,
            "short_url": absolute_short_url,
            "tracking_num": tracking_num,
            "trackings": trackings,
            "username": request.user.username,
            "page": page,
        },
    )


@login_required(login_url="/login")
def logout_view(request: HttpRequest):
    logout(request)
    return HttpResponse(
        status=302, reason="Redirecting", headers={"Location": "/login"}
    )


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponse(
            status=302, reason="Redirecting", headers={"Location": "/shorten"}
        )
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(
                status=302, reason="Redirecting", headers={"Location": "/shorten"}
            )
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "login.html")
    return render(request, "login.html")
