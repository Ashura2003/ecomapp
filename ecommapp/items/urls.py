from django.urls import path

from .views import *

urlpatterns = [
    path('/get', RetrieveItemView.as_view(), name='getallitems'),
    path('/get/pk', RetrieveItemView.as_view(), name = 'getsingleitem'),
    path('create/', RegisterItemView.as_view(), name='createitem'),
    path('update/', RegisterItemView.as_view(), name= 'update'),
    path('delete/', RegisterItemView.as_view(), name = 'delete')
]