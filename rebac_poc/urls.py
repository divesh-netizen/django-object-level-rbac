from django.contrib import admin
from django.urls import path

from core.views import access_probe_view, my_cameras_view, my_machines_view, my_stores_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/stores/', my_stores_view, name='my-stores'),
    path('api/cameras/', my_cameras_view, name='my-cameras'),
    path('api/machines/', my_machines_view, name='my-machines'),
    path('api/cameras/<int:camera_id>/probe/', access_probe_view, name='camera-probe'),
]
