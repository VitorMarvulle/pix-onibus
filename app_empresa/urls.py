from django.urls import path
from . import views


urlpatterns = [
    path('empresa', views.login, name='empresa'),
    path('add_linha/', views.add_linha, name='add_linha'),
    path('editar_linha/<int:id>/', views.editar_linha, name='editar_linha'),
    path('excluir_linha/<int:id>/',views.excluir_linha, name='excluir_linha'),
    path('add_motorista/', views.add_motorista, name='add_motorista'),

    # app_Empresa
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home_motorista/', views.home_motorista, name='home_motorista'),
    path('lista_motorista/', views.lista_motorista, name='lista_motorista'),
    path('linha_motorista/', views.linha_motorista, name='linha_motorista'),
    path('login/', views.login, name='login'),
    path('confirmacao/', views.confirmacao, name='confirmacao'),
    
    path('api/validar-bilhete/', views.validar_bilhete, name='validar_bilhete'),

]