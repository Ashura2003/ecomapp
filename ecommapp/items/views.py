from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item
from .permission import IsAdminOrSeller
from .serializer import ItemSerializer


# Create your views here.
class RegisterItemView(APIView):
    
    permission_classes = [IsAdminOrSeller]

    def post(self, request ):
        serializer = ItemSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            item = Item.objects.get(pk = pk)
        except Item.DoesNotExist:
            return Response({"error": "Item not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemSerializer(data= request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, pk):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({"error" : "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            item.delete()
            return Response({"message" : "Item deleted sucessfully"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"message" : "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class RetrieveItemView(APIView):
    
    permission_classes = [AllowAny]

    def get(self, pk):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({"error" : "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(item, status=status.HTTP_200_OK)
    
class RetrieveAllItemsView(APIView):
    """
    View to retrieve all items in the e-commerce application.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)