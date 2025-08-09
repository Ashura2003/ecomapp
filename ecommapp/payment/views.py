import stripe
from decouple import config
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import requests

stripe.api_key = config('STRIPE_SECRET_KEY')

class PaymentAPIView(APIView):
    def post(self,request,*args,**kwargs):
        token = request.POST.get('token')
        amount = request.POST.get('amount')
        payload = {
            "token":token,
            "amount":amount,
        }
        headers = {
            "Authorization": "Key {}".format(settings.PAYMENT_SECRET_KEY)
        }
        try:
            response = requests.post(settings.PAYMENT_VERIFY_URL,payload,headers=headers)
            if response.status_code == 200 :
                return Response({
                    'status':True,
                    'details':response.json(),
                })

            else:
                return Response({
                    'status':False,
                    'details':response.json(),
                })

        except requests.exceptions.HTTPError as e:
            return Response({
                'status':False,
                'details':response.json(),
            })