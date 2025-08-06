from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email', 'first_name', 'last_name']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'quantity']
    list_filter = ['user', 'item']
    search_fields = ['user__username', 'item__name']

    