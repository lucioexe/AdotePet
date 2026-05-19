from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('animal/<int:pk>/', views.detalhe, name='detalhe'),
]

