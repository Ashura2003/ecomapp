# users/urls.py
from django.urls import path

from .views import CartView, CustomLoginView, RegisterUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),  # POST username/email + password -> token
    path ('cart/', CartView.as_view(), name='cart'), # Route for the add to cart functionality
    path ('cart/<int:pk>/', CartView.as_view(), name='delete_cart_item'), # Route for deleting a cart item
]
