from django.contrib import admin
from django.urls import path,include
from store import urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('website/',include('store.urls'),name='store'),
]