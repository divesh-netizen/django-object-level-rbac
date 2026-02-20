from django.core.management.base import BaseCommand
from django.db import transaction
from guardian.shortcuts import assign_perm

from core.models import Camera, Machine, Organization, Store, User
from core.roles import ORG_ADMIN, STORE_MANAGER, VIEWER, assign_role


class Command(BaseCommand):
    help = 'Seed demo hierarchy and object-level permissions for ReBAC PoC.'

    @transaction.atomic
    def handle(self, *args, **options):
        User.objects.all().delete()
        Machine.objects.all().delete()
        Camera.objects.all().delete()
        Store.objects.all().delete()
        Organization.objects.all().delete()

        org_a = Organization.objects.create(name='Org Alpha', address='10 Main Street')
        org_b = Organization.objects.create(name='Org Beta', address='200 Side Avenue')

        store_a1 = Store.objects.create(name='Alpha Downtown', client_id=org_a, address='Downtown')
        store_a2 = Store.objects.create(name='Alpha Uptown', client_id=org_a, address='Uptown')
        store_b1 = Store.objects.create(name='Beta Central', client_id=org_b, address='Central')

        cam_a1_1 = Camera.objects.create(channel_name='A1-Entrance', store=store_a1)
        cam_a1_2 = Camera.objects.create(channel_name='A1-Backroom', store=store_a1)
        cam_a2_1 = Camera.objects.create(channel_name='A2-Checkout', store=store_a2)
        cam_b1_1 = Camera.objects.create(channel_name='B1-Parking', store=store_b1)

        machine_a1 = Machine.objects.create(
            name='AlphaEdge-01',
            description='Edge box for Downtown',
            mac_id='AA:AA:AA:AA:01',
            secret_key='secret-1',
            client_id=org_a,
            store=store_a1,
            host_address='10.0.0.11',
        )
        machine_a2 = Machine.objects.create(
            name='AlphaEdge-02',
            description='Edge box for Uptown',
            mac_id='AA:AA:AA:AA:02',
            secret_key='secret-2',
            client_id=org_a,
            store=store_a2,
            host_address='10.0.0.12',
        )
        machine_b1 = Machine.objects.create(
            name='BetaEdge-01',
            description='Edge box for Beta Central',
            mac_id='BB:BB:BB:BB:01',
            secret_key='secret-3',
            client_id=org_b,
            store=store_b1,
            host_address='10.1.0.21',
        )

        machine_a1.cameras.add(cam_a1_1, cam_a1_2)
        machine_a2.cameras.add(cam_a2_1)
        machine_b1.cameras.add(cam_b1_1)

        org_admin = User.objects.create_user(
            username='org_admin', password='pass1234', organization=org_a, email='org_admin@example.com'
        )
        store_manager = User.objects.create_user(
            username='store_manager', password='pass1234', organization=org_a, email='store_manager@example.com'
        )
        single_camera_user = User.objects.create_user(
            username='camera_viewer', password='pass1234', organization=org_a, email='camera_viewer@example.com'
        )

        assign_role(org_admin, ORG_ADMIN, org_a)
        assign_role(store_manager, STORE_MANAGER, store_a1)
        assign_role(single_camera_user, VIEWER, store_a1)
        assign_perm('core.view_camera', single_camera_user, cam_a1_2)

        self.stdout.write(self.style.SUCCESS('Seeded demo data successfully.'))
        self.stdout.write('Users (password=pass1234): org_admin, store_manager, camera_viewer')
