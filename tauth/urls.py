from django.urls import path

from tauth.views import admin_oauth


urlpatterns = [path("admin/__oauth__/", admin_oauth, name="admin_oauth")]
