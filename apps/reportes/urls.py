from django.urls import path
from .views import reportes

urlpatterns = [
    path('reportes/', reportes, name='reportes'),
]
