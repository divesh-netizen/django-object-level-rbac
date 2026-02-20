from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('edit_organization', 'Can edit organization data'),
        ]

    def __str__(self) -> str:
        return str(self.name)


class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.username)


class Store(models.Model):
    name = models.CharField(max_length=255)
    client_id = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='stores')
    address = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ('edit_store', 'Can edit store data'),
        ]

    def __str__(self) -> str:
        return f'{self.name} (org={self.client_id_id})'


class Camera(models.Model):
    channel_name = models.CharField(max_length=255)
    store = models.ForeignKey(Store, models.CASCADE, related_name='cameras')
    create_datetime = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    modified_datetime = models.DateTimeField(blank=True, null=True, auto_now=True)
    data = models.JSONField(default=dict, blank=True)
    rtsp_ip = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    reid_order = models.IntegerField(null=True, blank=True)

    class Meta:
        permissions = [
            ('edit_camera', 'Can edit camera data'),
        ]

    def __str__(self) -> str:
        return f'{self.channel_name}, Store id={self.store_id}'

    def add_metadata(self, key, value):
        self.data[key] = value
        self.save()

    def get_metadata(self, key):
        return self.data.get(key, None)


class Machine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True, default='', max_length=200)
    mac_id = models.CharField(max_length=100, unique=True)
    secret_key = models.CharField(max_length=1000)
    client_id = models.ForeignKey(Organization, on_delete=models.CASCADE)
    store = models.ForeignKey('Store', on_delete=models.RESTRICT, related_name='machines')
    host_address = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    machine_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    cameras = models.ManyToManyField(Camera, through='MachineCamera', related_name='machine')

    class Meta:
        permissions = [
            ('edit_machine', 'Can edit machine data'),
        ]

    def clean(self):
        if not self.store_id:
            return
        if self.client_id_id != self.store.client_id_id:
            raise ValidationError(
                {'store': 'Selected store does not belong to the selected organization (client).'}
            )

    def __str__(self) -> str:
        return f'{self.id},{self.name}, Client:{self.client_id.name}'


class MachineCamera(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('machine', 'camera')
