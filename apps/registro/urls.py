from django.urls import path
from .views import raee_registrar, raee_mis_registros

urlpatterns = [
    path('raee/registrar/', raee_registrar, name='raee_registrar'),
    path('raee/mis-registros/', raee_mis_registros, name='raee_mis_registros'),
]
