from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quantidade/', views.quantidade, name='quantidade'),
    path('formulario/', csrf_exempt(views.formulario), name='formulario'),
    path('pagamento/', csrf_exempt(views.pagamento), name='pagamento'),
    path('check-payment-status/', views.check_payment_status, name='check_payment_status'),
    path('bilhete/', views.bilhete, name='bilhete'),
]