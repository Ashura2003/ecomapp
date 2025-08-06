# users/urls.py
from django.urls import path
from .views import RegisterUserView, CustomLoginView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),  # POST username/email + password -> token
]
