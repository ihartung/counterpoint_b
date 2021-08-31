from django.contrib import admin
from django.urls import path
from main.views import counterpoint
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('counterpoint', counterpoint),
    path('csrf', views.csrf),
    path('ping', views.ping),
]
