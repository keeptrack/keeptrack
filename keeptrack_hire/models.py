from django.db import models

from hire.models import HireRequest
from equipment.models import Asset


class AllocatedEquipment(models.Model):
    request = models.ForeignKey(HireRequest, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    discounted_price = models.DecimalField(max_digits=8, decimal_places=2,
                                           blank=True, null=True)


class AllocatedCustomItems(models.Model):
    request = models.ForeignKey(HireRequest, on_delete=models.CASCADE)

    text = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=8, decimal_places=2)
