from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('games/', include('gcf.urls')),
    path('admin/', admin.site.urls),
]
