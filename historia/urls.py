from django.urls import path
from .views import *
urlpatterns = [
	path('lista-historia/colegio-Assisi', lista_historia_eskola, name="lista-historia-eskola"),
	path('add-historia/colegio-Assisi', add_historia, name="add-historia"),
	path('update-historia/<str:hashid>', updatehistoria, name="update-historia"),
	# path('delete-horario/<str:id_hor>', deletehor, name="deletehor"),
	# path('dashboard/report/e/active/Horario/', EReportListActiveHorario, name="e-active-Horario"),
]