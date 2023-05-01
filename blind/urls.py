from django.contrib import admin
from django.urls import path, include

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "blind"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.reservation, name='reservation'),
    path("login/", views.login_view.as_view(), name="log_in"),
    path("logout/", views.log_out, name="log_out"),
    # path("signup/", views.sign_up, name="sign_up"),
    path("accounts/", include('allauth.urls'))
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) +static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
