from django.db import models
from django.urls import reverse

from equipment.models import Asset


class HireRequest(models.Model):
    # Hire details
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254)
    cid = models.CharField(max_length=16, blank=True, null=True)
    is_event = False
    is_hidden = models.BooleanField(default=False)
    colour = models.CharField(max_length=7, default="#000000")

    # Hire info.
    hire_from = models.DateField(auto_now=False, auto_now_add=False)
    hire_to = models.DateField(auto_now=False, auto_now_add=False)
    description = models.TextField()
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2,
                                           blank=True, null=True)

    # Metadata.
    # If we're hiring on behalf of society
    for_csp = models.IntegerField(blank=True, null=True)
    # Hire requests must be approved first.
    approved = models.BooleanField(default=False)
    # If we want to reject 
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return f'Hire({self.name}, {self.hire_from})'

    @property
    def get_html_url(self):
        url = reverse('cal:hire_edit', args=(self.id,))
        return f'<a href="{url}"> {self.name} </a>'


class Event(models.Model):
    # Event Details
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254)
    cid = models.CharField(max_length=16, blank=True, null=True)
    is_event = True
    is_hidden = models.BooleanField(default=False)
    colour = models.CharField(max_length=7, default="#000000")

    # Hire info.
    event_from = models.DateField(auto_now=False, auto_now_add=False)
    event_to = models.DateField(auto_now=False, auto_now_add=False)
    description = models.TextField()

    def __str__(self):
        return f'Event({self.name}, {self.event_from})'

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.name} </a>'
