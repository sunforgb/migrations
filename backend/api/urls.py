from django.urls import path, include
from .views import *

urlpatterns = [
    path('employees/', EmployeeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('employees/<int:pk>', EmployeeViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('migrants/', MigrantViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('migrants/<int:pk>', MigrantViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('statements/', RegistrationStatementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('statements/<int:pk>', RegistrationStatementViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('unstatements/', UnRegistrationStatementViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('unstatements/<int:pk>', UnRegistrationStatementViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),

]