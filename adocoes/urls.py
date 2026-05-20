from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('animal/<int:pk>/', views.detalhe, name='detalhe'),
    path('como-adotar/', views.como_adotar, name='como-adotar'),
    path('sobre-nos/', views.sobre_nos, name='sobre-nos'),
    path('ongs-parceiras/', views.ongs, name='ongs-parceiras'),
    path('cadastro/', views.view_cadastro, name='cadastro'),
    path('login/', views.view_login, name='login'),
    path('logout/', views.view_logout, name='logout'),
    path('perfil/', views.view_perfil, name='perfil'),
]

