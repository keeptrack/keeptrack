from django.db import models

from hire.models import HireRequest
from equipment.models import Asset

class AllocatedEquipment(models.Model):
    request = models.ForeignKey(HireRequest, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
