from django.contrib import admin

from .models import AllocatedEquipment

@admin.register(AllocatedEquipment)
class AllocatedEquipmentAdmin(admin.ModelAdmin):
    pass
