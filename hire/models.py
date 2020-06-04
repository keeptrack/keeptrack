from django.db import models


# Hire request.
from django.urls import reverse


class HireRequest(models.Model):
    # Hire details
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254)
    cid = models.CharField(max_length=16, blank=True, null=True)

    # Hire info.
    hire_from = models.DateField(auto_now=False, auto_now_add=False)
    hire_to = models.DateField(auto_now=False, auto_now_add=False)
    description = models.TextField()
    # TODO: requested_assets = models.ManyToManyField(OfferedServices)

    # Metadata.
    # If we're hiring on behalf of society
    for_csp = models.IntegerField(blank=True, null=True)
    # Hire requests must be approved first.
    approved = models.BooleanField(default=False)
    # If we want to reject 
    rejected = models.BooleanField(default=False)
    # TODO: One hire is associated with many assets.
    # allocated_assets = models.ManyToManyField(Asset, through='AllocatedEquipment')

    def __str__(self):
        return f"Hire({self.name}, {self.hire_from})"

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.name} </a>'
