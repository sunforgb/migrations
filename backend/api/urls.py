from django.urls import path, include
from .views import *

urlpatterns = [
    path('employees/', EmployeeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('employees/<int:pk>', EmployeeViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}))
]