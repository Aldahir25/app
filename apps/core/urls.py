"""Rutas del núcleo: landing, autenticación y dashboard."""
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import dashboard, home, login_view, register_view

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('registro/', register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]
