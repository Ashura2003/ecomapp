# serializers.py

from rest_framework import serializers

class CheckoutSerializer(serializers.Serializer):
    payment_method_id = serializers.CharField(required=True)
