from django.urls import path
from .views import *

urlpatterns = [
	path('lista-horario/', Listahor, name="Listahor"),
	path('add-horario/', add_hor, name="add_hor"),
	path('update-horario/<str:hashid>', updatehor, name="updatehor"),
	path('delete-horario/<str:id_hor>', deletehor, name="deletehor"),
	path('dashboard/report/e/active/Horario/', EReportListActiveHorario, name="e-active-Horario"),
	path('Horariu/<str:pk>/klasse/',HorKlasseList, name="HorKlasseList"),


	
	path('horarioloron/', horario_por_loron, name='horario_por_loron'),

	# Professor
    path('lista-horario/funsionariu/', ListahorFun, name="ListahorFun"),
	# Professor
    path('lista-horario/estudante/', ListahorEst, name="ListahorEst"),
]