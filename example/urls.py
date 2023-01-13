"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path,  include
from authlib import views
from authlib.google import GoogleOAuth2Client

urlpatterns = [
    #re_path(r"", include("authlib.admin_oauth.urls")),
    re_path(r"", include("tauth.urls")),
    path('admin/', admin.site.urls),
    re_path(
        r"^login/$",
        views.login,
        name="login",
    ),
    re_path(
        r"^oauth/google/$",
        views.oauth2,
        {
            "client_class": GoogleOAuth2Client,
        },
        name="accounts_oauth_google",
    ),
    re_path(
        r"^email/$",
        views.email_registration,
        name="email_registration",
    ),
    re_path(
        r"^email/(?P<code>[^/]+)/$",
        views.email_registration,
        name="email_registration_confirm",
    ),
    re_path(
        r"^logout/$",
        views.logout,
        name="logout",
    ),
]
