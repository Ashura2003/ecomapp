from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartItem
from .serializer import CustomCartItemSerializer, UserSerializer

User = get_user_model()

class RegisterUserView(APIView):
    '''
    View for user registration.
    '''
    permission_classes = [AllowAny]

    def post(self, request):
        '''
        Handle user registration.
        '''
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomLoginView(APIView):
    """
    Login view that accepts either username+password or email+password.
    Returns DRF Token + small user payload.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        '''
        Handle user login.
        '''
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        print(username,email)
        print(password)

        if not password:
            return Response({'detail': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # If username is missing but email is provided, resolve username by email
        if not username and email:
            try:
                user_by_email = User.objects.get(email=email)
                username = user_by_email.get_username()
            except User.DoesNotExist:
                return Response({'non_field_errors': ['No user with that email.']}, status=status.HTTP_400_BAD_REQUEST)

        if not username:
            return Response({'non_field_errors': ['username or email is required.']}, status=status.HTTP_400_BAD_REQUEST)


        user = authenticate(username=username, password=password)
        print(user)
        if not user:
            # Generic error (keeps details minimal). While debugging you can log more server-side.
            return Response({'non_field_errors': ['Unable to log in with provided credentials.']}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({'non_field_errors': ['User account is disabled.']}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        # Optional: include more user data via serializer
        user_data = UserSerializer(user).data

        return Response({
            'token': token.key,
            'user': user_data
        }, status=status.HTTP_200_OK)
class UserUpdateView(APIView):
    '''
    View for updating user details.
    '''
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(APIView):
    '''
    View for deleting a user account.
    '''
    def delete(self, request, *args, **kwargs):
        user = request.user
        if user.delete():
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif not user.delete():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)    
    

class CartView(APIView):
    '''
    This View is used for the add to cart functionality of the app
    '''

    def post(self, request):
        serializer = CustomCartItemSerializer(data = request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        serializer = CustomCartItemSerializer(data = request.data , context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, pk):
        cart = CartItem.objects.get(pk=pk)
        if cart:
            cart.delete()
            return Response({"message": "Cart item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        serializer = CustomCartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
