from django.contrib import admin

from .models import AllocatedEquipment, AllocatedCustomItems

@admin.register(AllocatedEquipment)
class AllocatedEquipmentAdmin(admin.ModelAdmin):
    pass

@admin.register(AllocatedCustomItems)
class AllocatedCustomItemsAdmin(admin.ModelAdmin):
    pass
