from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('animal/<int:pk>/', views.detalhe, name='detalhe'),
    path('como-adotar/', views.como_adotar, name='como-adotar'),
    path('sobre-nos/', views.sobre_nos, name='sobre-nos'),
    path('ongs-parceiras/', views.ongs, name='ongs-parceiras'),
]

