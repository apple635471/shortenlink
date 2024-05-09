"""shortenlink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from .facebook_views import oauth2_login as facebook_login
from .facebook_views import oauth2_callback as facebook_callback

urlpatterns = [
    path("", include("app.urls")),
    path("admin/", admin.site.urls),
    path("accounts/facebook/login/", facebook_login, name="facebook_login"),
    path(
        "accounts/facebook/login/callback/", facebook_callback, name="facebook_callback"
    ),
    path("accounts/", include("allauth.urls")),
]
