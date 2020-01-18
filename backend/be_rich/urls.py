from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/transactions/', include('backend.transactions.urls')),
    path('api/', include('backend.api.urls')),
    path('', include('frontend.urls')),
]
