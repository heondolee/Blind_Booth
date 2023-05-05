from django.contrib import admin
from django.urls import path, include

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "blind"

urlpatterns = [
    path('manage/', admin.site.urls),
    path('', views.reservation, name='reservation'),
    path('reserve_page/<int:day>/<int:slot>', views.reserve_page, name='reserve_page'),
    path("logout/", views.log_out, name="log_out"),
    path("info_update/", views.info_update, name="info_update"),
    path("accounts/", include('allauth.urls')),
    path("detail/<int:id>/<int:gender>", views.detail, name="detail"),
    path('csvToModel', views.csvToModel, name='csvToModel'), # db 설정용 url
    path('dbToCsv', views.dbToCsv, name='dbToCsv'), 

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

