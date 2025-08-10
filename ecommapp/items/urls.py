from django.urls import path

from .views import (RegisterItemView, RetrieveAllItemsView, RetrieveItemView,
                    SearchItemsView)

urlpatterns = [
    path('items/', RegisterItemView.as_view(), name = 'retrieve'),
    path('items/<int:pk>', RegisterItemView().as_view, name= 'update'),
    path('items/get/<int:pk>', RetrieveItemView().as_view, name= 'get'),
    path('items/get_all/', RetrieveAllItemsView().as_view(), name= 'retrieve'),
    path('items/search', SearchItemsView.as_view(), name= 'search')
]