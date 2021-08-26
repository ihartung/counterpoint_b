from django.contrib import admin
from django.urls import path
from main.views import counterpoint

urlpatterns = [
    path('admin/', admin.site.urls),
    path('counterpoint', counterpoint),
]
