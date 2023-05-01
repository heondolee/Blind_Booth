from django.contrib import admin
from django.urls import path, include

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "blind"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.reservation, name='reservation'),
    path("logout/", views.log_out, name="log_out"),
    path("info_update/", views.info_update, name="info_update"),
    path("accounts/", include('allauth.urls'))
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
