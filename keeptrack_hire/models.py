from django.db import models

from hire.models import HireRequest

class AllocatedEquipment(models.Model):
    request = models.ForeignKey(HireRequest, on_delete=models.CASCADE)
    # euqipment = models.ForeignKey(Asset, null=True)
