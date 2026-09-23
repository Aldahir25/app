from django.urls import path
from .views import educacion, evaluacion

urlpatterns = [
    path('educacion/', educacion, name='educacion'),
    path('educacion/evaluacion/', evaluacion, name='evaluacion'),
]
