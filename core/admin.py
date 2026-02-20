from django.contrib import admin

from core.models import Camera, Machine, MachineCamera, Organization, Store, User

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Store)
admin.site.register(Camera)
admin.site.register(Machine)
admin.site.register(MachineCamera)
