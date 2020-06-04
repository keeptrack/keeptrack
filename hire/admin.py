from django.contrib import admin
from hire.models import HireRequest


@admin.register(HireRequest)
class HireRequestAdmin(admin.ModelAdmin):
    pass
