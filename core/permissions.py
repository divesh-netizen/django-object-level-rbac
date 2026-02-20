from typing import Iterable

from django.db.models import Model

from core.models import Camera, Machine, Organization, Store

ACTION_TO_CODENAME = {
    'view': {
        Organization: 'view_organization',
        Store: 'view_store',
        Camera: 'view_camera',
        Machine: 'view_machine',
    },
    'edit': {
        Organization: 'edit_organization',
        Store: 'edit_store',
        Camera: 'edit_camera',
        Machine: 'edit_machine',
    },
}


def _permission_name(action: str, obj: Model) -> str:
    try:
        codename = ACTION_TO_CODENAME[action][type(obj)]
    except KeyError as error:
        raise ValueError(f'Unsupported permission action/object combination: {action} + {type(obj).__name__}') from error
    return f'{obj._meta.app_label}.{codename}'


def _parent_chain(obj: Model) -> Iterable[Model]:
    if isinstance(obj, Organization):
        return []
    if isinstance(obj, Store):
        return [obj.client_id]
    if isinstance(obj, Camera):
        return [obj.store, obj.store.client_id]
    if isinstance(obj, Machine):
        return [obj.store, obj.store.client_id]
    raise ValueError(f'Unsupported object type: {type(obj).__name__}')


def has_object_access(user, obj: Model, action: str) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True

    if user.has_perm(_permission_name(action, obj), obj):
        return True

    for parent in _parent_chain(obj):
        if user.has_perm(_permission_name(action, parent), parent):
            return True

    return False
