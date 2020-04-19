from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('form/', include('form.urls')),
    path('admin/', admin.site.urls),
]
