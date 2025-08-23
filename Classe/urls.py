from django.urls import path
from .views import *

urlpatterns = [
	path('lista-classe/', ListaClasse, name="ListaClasse"),
	path('add-classe/', addclasse, name="addclasse"),
	path('update-classe/<str:hashid>', updatecl, name="updatecl"),
	path('delete-classe/<str:id_classe>', Deletecl, name="Deletecl"),

	path('ajax/load-Classe/', load_Classe, name='ajax_load_classe'),
]