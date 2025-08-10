# views.py

import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartItem, Order, OrderItem
from .serializer import CheckoutSerializer

stripe.api_key = settings.PAYMENT_SECRET_KEY

class CheckoutView(APIView):
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        payment_method_id = serializer.validated_data['payment_method_id']

        # Get cart items
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total amount
        total_amount = sum(ci.item.price * ci.quantity for ci in cart_items)

        try:
            # Create and confirm PaymentIntent on Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=int(total_amount * 100),  # amount in paisa
                currency='npr',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
                return_url="http://127.0.0.1:8000/success"
            )

            # Handle payment actions like 3D Secure if required
            if payment_intent.status == 'requires_action':
                return Response({
                    'requires_action': True,
                    'payment_intent_client_secret': payment_intent.client_secret
                }, status=status.HTTP_200_OK)

            if payment_intent.status != 'succeeded':
                return Response({'error': 'Payment not successful.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create Order and OrderItems
            order = Order.objects.create(
                user=user,
                total_amount=total_amount,
                payment_intent=payment_intent.id
            )

            for ci in cart_items:
                OrderItem.objects.create(
                    order=order,
                    item=ci.item,
                    quantity=ci.quantity,
                    price_per_item=ci.item.price
                )

            # Clear user's cart
            cart_items.delete()

            return Response({'message': 'Payment successful and order created!'}, status=status.HTTP_200_OK)

        except stripe.error.CardError as e:
            return Response({'error': str(e.user_message)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
