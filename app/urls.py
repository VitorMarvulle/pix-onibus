from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quantidade/', views.quantidade, name='quantidade'),
    path('formulario/', views.formulario, name='formulario'),
    path('pagamento/', views.pagamento, name='pagamento'),
    path('bilhete/', views.bilhete, name='bilhete'),
]