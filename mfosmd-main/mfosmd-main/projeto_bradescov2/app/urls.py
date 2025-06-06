from django.urls import path
from .views import RegistroView, LoginView, ValoresReceberView, CustomLoginView, MeuValorView
from .views_apialy import consultar_valores_externos

urlpatterns = [
    path('registro/', RegistroView.as_view()),
    path('login/', LoginView.as_view()),
    path('valores-a-receber/', ValoresReceberView.as_view()),
    path('token/', CustomLoginView.as_view()), 
    path('meu-valor/', MeuValorView.as_view()),
    path('consultar-valores/', consultar_valores_externos)
]
