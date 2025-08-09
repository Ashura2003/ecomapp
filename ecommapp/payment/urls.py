from django.urls import path

from .views import PaymentAPIView

urlpatterns = [
    path('make_payment/', PaymentAPIView.as_view(), name='make_payment')
]