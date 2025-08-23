from django.urls import path
from .views import *

urlpatterns = [
	path('lista-turma/', listaTurma, name="listaTurma"),
	path('add-turma/', addTurma, name="addTurma"),
	path('update-turma/<str:hashid>', updateTurma, name="updateTurma"),
	path('delete-turma/<str:id_turma>', deleteTurma, name="deleteTurma"),

	path('ajax/load-Turma/', load_Turma, name='ajax_load_Turma'),
]