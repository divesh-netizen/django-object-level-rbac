from dataclasses import dataclass

from guardian.shortcuts import assign_perm

from core.models import Organization, Store


@dataclass(frozen=True)
class Role:
    name: str
    permissions: tuple[str, ...]


ORG_ADMIN = Role(
    name='ORG_ADMIN',
    permissions=(
        'view_organization',
        'edit_organization',
        'view_store',
        'edit_store',
        'view_camera',
        'edit_camera',
        'view_machine',
        'edit_machine',
    ),
)

STORE_MANAGER = Role(
    name='STORE_MANAGER',
    permissions=(
        'view_store',
        'edit_store',
        'view_camera',
        'edit_camera',
        'view_machine',
        'edit_machine',
    ),
)

VIEWER = Role(
    name='VIEWER',
    permissions=(
        'view_store',
        'view_camera',
        'view_machine',
    ),
)


def assign_role(user, role: Role, obj: Organization | Store) -> None:
    app_label = obj._meta.app_label
    for codename in role.permissions:
        assign_perm(f'{app_label}.{codename}', user, obj)
