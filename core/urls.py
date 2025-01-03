from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit/', views.handle_input, name='handle_input'),
    path('send_image/', views.send_image, name='send_image'),
    path('api/result/', views.result_json_view, name='result_json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)