from django.db import models


# Hire request.
class HireRequest(models.Model):
    # Hire details
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254)
    cid = models.CharField(max_length=16, blank=True)

    # Hire info.
    hire_from = models.DateField(auto_now=False, auto_now_add=False)
    hire_to = models.DateField(auto_now=False, auto_now_add=False)
    description = models.TextField()

    # Metadata.
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"Hire({self.name}, {self.hire_from})"
