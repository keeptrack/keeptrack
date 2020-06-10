from django.db import models


class Asset(models.Model):
    uid = models.IntegerField(primary_key=True)
    category = models.TextField()
    brand = models.TextField()
    name = models.TextField()
    condition = models.TextField()
    value = models.DecimalField(max_digits=9, decimal_places=2)
    storage_location = models.TextField()
    hire_price = models.DecimalField(max_digits=9, decimal_places=2)
    notes = models.TextField()

    def to_dict(self):
        return {
            "uid": self.uid,
            "category": self.category,
            "brand": self.brand,
            "name": self.name,
            "condition": self.condition,
            "value": self.value,
            "storage_location": self.storage_location,
            "hire_price": self.hire_price,
            "notes": self.notes,
            "next_hire_date": self.next_hire_date()
        }

    def next_hire_date(self):
        return "None"
