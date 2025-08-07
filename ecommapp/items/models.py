from django.db import models


# Custom item model for the items in the e-commerce application
class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    

    def __str__(self):
        return self.name
