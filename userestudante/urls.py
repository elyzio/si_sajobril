from django.urls import path
from . import views
urlpatterns = [
    path('meus_detalhes/', views.detalho_estudante, name='detalho_estudante'),
    path('DetailValoresEstudante/meo-Valor',views.DetailValoresEstudante,name="DetailValoresEstudante"),
    path('atualizar_dados/', views.atualizar_dados, name='atualizar_dados'),
    # path('home-login/', homelogin, name="home-login"),
    
    
]
