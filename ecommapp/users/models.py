# Custom user model for the e-commerce application
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from items.models import Item


class User(AbstractUser):
    USERTYPE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=10, choices=USERTYPE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # amount in the user's cart

    def __str__(self):
        return f"{self.quantity} x {self.item.name} for {self.user.username}"

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ('user', 'item')
