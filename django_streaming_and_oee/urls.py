
from django.contrib import admin
from django.urls import path, include
from videostreaming.views import Home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('videostreaming.urls')),
    path('api/v1/',include('machines.urls')),
    path('',Home.as_view())
]
