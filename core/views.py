from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404

from core.models import Camera, Machine, Store
from core.permissions import has_object_access


@login_required
def my_stores_view(request: HttpRequest):
    visible = [
        {'id': store.id, 'name': store.name, 'organization_id': store.client_id_id}
        for store in Store.objects.select_related('client_id')
        if has_object_access(request.user, store, 'view')
    ]
    return JsonResponse({'count': len(visible), 'results': visible})


@login_required
def my_cameras_view(request: HttpRequest):
    visible = [
        {'id': camera.id, 'channel_name': camera.channel_name, 'store_id': camera.store_id}
        for camera in Camera.objects.select_related('store', 'store__client_id')
        if has_object_access(request.user, camera, 'view')
    ]
    return JsonResponse({'count': len(visible), 'results': visible})


@login_required
def my_machines_view(request: HttpRequest):
    visible = [
        {'id': machine.id, 'name': machine.name, 'store_id': machine.store_id}
        for machine in Machine.objects.select_related('store', 'store__client_id')
        if has_object_access(request.user, machine, 'view')
    ]
    return JsonResponse({'count': len(visible), 'results': visible})


@login_required
def access_probe_view(request: HttpRequest, camera_id: int):
    camera = get_object_or_404(Camera.objects.select_related('store', 'store__client_id'), id=camera_id)
    if not has_object_access(request.user, camera, 'view'):
        return HttpResponseForbidden('Access denied for this camera')
    return JsonResponse({'id': camera.id, 'channel_name': camera.channel_name, 'store_id': camera.store_id})
