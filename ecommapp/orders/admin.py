from django.contrib import admin

from .models import Order


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_amount', 'payment_intent')
    search_fields = ('user__username', 'payment_intent')
    list_filter = ('created_at',)