# users/urls.py
from django.urls import path

from .views import AddToCartView, CustomLoginView, RegisterUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),  # POST username/email + password -> token
    path ('cart/', AddToCartView.as_view(), name='cart') # Route for the add to cart functionality
]
